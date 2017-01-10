import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from schedule.models import Event

from customLibrary.views_lib import get_userdetails, ajax_response, obj_to_json_response, string_to_dict, \
    get_ist_datetime, get_utc_datetime, debugFileLog, empty_list_for_none, \
    timeit, mail_exception
from playlistManagement.models import Playlist
from scheduleManagement.helpers import event_dict_from_timeline
from scheduleManagement.models import Schedule, SchedulePlaylists, ScheduleScreens, SchedulePane
from scheduleManagement.serializers import default_schedule_serializer
from screenManagement.models import Screen, Group
from layoutManagement.models import Layout


# Create your views here.
@login_required
def index(request):
    return render(request, 'scheduleManagement/schedule_index.html')


def add_schedule(request):
    return render(request, 'scheduleManagement/schedule_details.html')


def upsert_schedule_screens(user_details, schedule, schedule_screens):
    debugFileLog.info("inside upsert_schedule_screens")
    error = ''
    schedule_screen_id_list = []
    for item in schedule_screens:
        schedule_screen_id = int(item.get('schedule_screen_id'))
        if schedule_screen_id == -1:
            screen_id = int(item.get('screen_id'))
            screen = Screen.get_user_relevant_objects(user_details).get(screen_id=screen_id)
            entry = ScheduleScreens.objects.create(screen=screen, schedule=schedule)
            schedule_screen_id = entry.schedule_screen_id
        schedule_screen_id_list.append(schedule_screen_id)

    # Remove screens not in the schedule
    removed_schedule_screens = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=True).exclude(
        schedule_screen_id__in=schedule_screen_id_list)
    if removed_schedule_screens.exists():
        removed_schedule_screens.delete()
    success = True
    return success, error, schedule


def upsert_schedule_groups(user_details, schedule, schedule_groups):
    debugFileLog.info("inside upsert_schedule_groups")
    error = ''
    schedule_screen_id_list = []
    for item in schedule_groups:
        schedule_screen_id = int(item.get('schedule_screen_id'))
        if schedule_screen_id == -1:
            group_id = int(item.get('group_id'))
            group = Group.get_user_relevant_objects(user_details).get(group_id=group_id)
            # Adding one screen=NULL entry to handle the case of scheduling empty groups and later adding screens
            # into that empty group
            entry = ScheduleScreens(schedule=schedule, group=group)
            entry.save()
            schedule_screen_id = entry.schedule_screen_id
            for screen in group.screen_set.all():
                entry = ScheduleScreens(screen=screen, schedule=schedule, group=group)
                entry.save()
                schedule_screen_id_list.append(entry.schedule_screen_id)
        schedule_screen_id_list.append(schedule_screen_id)

    # Remove groups not in the schedule
    removed_schedule_groups = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=False).exclude(
        schedule_screen_id__in=schedule_screen_id_list)
    if removed_schedule_groups.exists():
        removed_schedule_groups.delete()
    success = True
    return success, error, schedule


def upsert_schedule_playlists(user_details, schedule_pane_id, schedule_playlists):
    debugFileLog.info("inside upsert_schedule_playlists")
    error = ''
    schedule_playlist_id_list = []
    for pos_index, item in enumerate(schedule_playlists):
        schedule_playlist_id = int(item.get('schedule_playlist_id'))
        playlist_id = int(item.get('playlist_id'))
        playlist_type = item.get('playlist_type')
        if playlist_type == Playlist.CONTENT or playlist_type == Playlist.WIDGET:
            playlist = Playlist.upsert_playlist_from_dict(playlist_dict=item, user_details=user_details, user_visible=False)
            playlist_id = playlist.playlist_id
        if playlist_type == Playlist.BLYNQ_TV:
            playlist = Playlist.get_blynq_content_playlists().get(playlist_id=playlist_id)
        else:
            playlist = Playlist.get_all_playlists(user_details).get(playlist_id=playlist_id)
        if schedule_playlist_id == -1:
            entry = SchedulePlaylists(schedule_pane_id=schedule_pane_id, playlist=playlist, position_index=pos_index)
            entry.save()
            schedule_playlist_id = entry.schedule_playlist_id
        else:
            entry = SchedulePlaylists.objects.get(schedule_playlist_id=schedule_playlist_id)
            entry.position_index = pos_index
            entry.save()
        schedule_playlist_id_list.append(schedule_playlist_id)

    # Remove playlists not in playlist_schedules
    removed_playlist_schedules = SchedulePlaylists.objects.filter(schedule_pane_id=schedule_pane_id).exclude(
        schedule_playlist_id__in=schedule_playlist_id_list)
    if removed_playlist_schedules.exists():
        removed_playlist_schedules.delete()
    return True, error


def upsert_schedule_panes(user_details, schedule, schedule_panes, layout):
    debugFileLog.info("inside upsert_schedule_panes")
    error = ''
    schedule_pane_id_list = []
    for item in schedule_panes:
        schedule_pane_id = int(item.get('schedule_pane_id'))
        schedule_playlists = empty_list_for_none(item.get('schedule_playlists'))
        schedule_widgets = empty_list_for_none(item.get('schedule_widgets'))
        schedule_playlists.extend(schedule_widgets)
        schedule_blynq_playlists = empty_list_for_none(item.get('schedule_blynq_playlists'))
        layout_pane = item.get('layout_pane')
        layout_pane_id = int(layout_pane.get('layout_pane_id'))
        mute_audio = item.get('mute_audio')
        timeline = item.get('timeline')
        is_always = timeline.get('is_always')
        all_day = timeline.get('all_day')
        recurrence_absolute = timeline.get('recurrence_absolute')
        if not recurrence_absolute:
            recurrence_absolute = False
        if schedule_playlists or schedule_blynq_playlists:
            event_dict, schedule = event_dict_from_timeline(timeline=timeline, schedule=schedule)
            event = Event(**event_dict)
            event.save()
        else:
            event = None
        if schedule_pane_id == -1:
            schedule_pane = SchedulePane(schedule=schedule, layout_pane_id=layout_pane_id, mute_audio=mute_audio,
                                         is_always=is_always, all_day=all_day, recurrence_absolute=recurrence_absolute,
                                         event=event)
            schedule_pane.save()
            schedule_pane_id = schedule_pane.schedule_pane_id
        else:
            schedule_pane = SchedulePane.objects.get(schedule_pane_id=schedule_pane_id)
            schedule_pane.schedule = schedule
            schedule_pane.layout_pane_id = layout_pane_id
            schedule_pane.is_always = is_always
            schedule_pane.all_day = all_day
            schedule_pane.mute_audio = mute_audio
            schedule_pane.recurrence_absolute = recurrence_absolute
            # Not deleting the event, to have the history of events
            schedule_pane.event = event
            schedule_pane.save()

        upsert_schedule_playlists(user_details=user_details, schedule_pane_id=schedule_pane_id,
                                  schedule_playlists=schedule_playlists)
        schedule_pane_id_list.append(schedule_pane_id)

    # Remove Schedule Panes which are not in the post request
    remove_schedule_panes = SchedulePane.objects.filter(schedule=schedule).exclude(
        schedule_pane_id__in=schedule_pane_id_list)
    if remove_schedule_panes.exists():
        remove_schedule_panes.delete()
    return True, error, schedule


@timeit
@transaction.atomic
@login_required
def upsert_schedule(request):
    debugFileLog.info("inside upsert_schedule")
    errors = []
    success = False
    user_details = get_userdetails(request)
    try:
        with transaction.atomic():
            # Extract data from request.body
            posted_data = string_to_dict(request.body)
            schedule_id = int(posted_data.get('schedule_id'))
            schedule_title = posted_data.get('schedule_title')
            schedule_description = posted_data.get('schedule_description')
            schedule_screens = posted_data.get('schedule_screens')
            schedule_groups = posted_data.get('schedule_groups')
            layout = posted_data.get('layout')
            schedule_panes = posted_data.get('schedule_panes')
            user_schedules = Schedule.get_user_relevant_objects(user_details=user_details)
            layout_id = int(layout.get('layout_id'))
            layout = Layout.objects.get(layout_id=layout_id)
            # upsert schedule
            if schedule_id == -1:
                schedule = Schedule(schedule_title=schedule_title, schedule_description=schedule_description,
                                    created_by=user_details, layout=layout, last_updated_by=user_details,
                                    organization=user_details.organization)
                schedule.save()
            else:
                schedule = user_schedules.get(schedule_id=schedule_id)
                schedule.schedule_title = schedule_title
                schedule.schedule_description = schedule_description
                schedule.layout = layout
                schedule.last_updated_by = user_details
            # schedule.save()

            success_screens, error, schedule = upsert_schedule_screens(user_details=user_details, schedule=schedule,
                                                                       schedule_screens=schedule_screens)
            errors.append(error)

            success_groups, error, schedule = upsert_schedule_groups(user_details=user_details, schedule=schedule,
                                                                     schedule_groups=schedule_groups)
            errors.append(error)

            success_panes, error, schedule = upsert_schedule_panes(user_details=user_details, schedule=schedule,
                                                                   schedule_panes=schedule_panes, layout=layout)
            success = success_screens and success_groups and success_panes
            errors.append(error)

            schedule.save()
    except Exception as e:
        success = False
        error = 'Error while upserting content to schedule'
        error_help_str = error + ', request body is ' + str(request.body)
        debugFileLog.exception(error_help_str)
        mail_exception(exception=e)
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def get_screen_schedules(request, screen_id):
    debugFileLog.info("inside get_screen_schedules")
    screen_id = int(screen_id)
    user_details = get_userdetails(request)
    screen_schedules = Schedule.get_user_relevant_objects(user_details).filter(screens__screen_id=screen_id).distinct()
    json_data = default_schedule_serializer(querySet=screen_schedules)
    return obj_to_json_response(json_data)


def get_group_schedules(request, group_id):
    debugFileLog.info("inside get_group_schedules")
    group_id = int(group_id)
    user_details = get_userdetails(request)
    group_schedule_id_list = ScheduleScreens.objects.filter(screen__isnull=True, group_id=group_id).values_list(
        'schedule_id', flat=True).distinct()
    group_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=group_schedule_id_list)
    json_data = default_schedule_serializer(querySet=group_schedules)
    return obj_to_json_response(json_data)


def get_schedules(request):
    """
    :param request:
    :return:
    [
        {
            timeline: {
                byweekno: null,
                recurrence_absolute: false,
                start_time: "05:30",
                interval: null,
                all_day: true,
                bymonthday: null,
                end_time: "05:29",
                frequency: "DAILY",
                is_always: true,
                byweekday: null,
                start_date: "2016/06/09",
                end_recurring_period: null
            },
            schedule_playlists: [
            {
                playlist_items: [
                {
                    display_time: 15,
                    is_folder: false,
                    title: "sachin",
                    url: "http://127.0.0.1:8000/media/usercontent/1/sachin.jpg",
                    playlist_item_id: 7,
                    content_type: "file/image/jpeg",
                    content_id: 11
                }],
                playlist_title: "first playlist",
                schedule_playlist_id: 23,
                playlist_id: 1
            }],
            schedule_id: 23,
            schedule_groups: [ ],
            schedule_screens: [
            {
                status: "Offline",
                city: {
                    city_id: 1,
                    city_name: "Hyderabad"
                },
                schedule_screen_id: 31,
                screen_name: "jaydev android emulator",
                screen_size: 32,
                groups: [
                {
                    group_name: "Group 1",
                    group_id: 1,
                    group_screen_id: 5
                }],
                address: "",
                resolution: "1190*768",
                screen_id: 1
            },
            {
                status: "Offline",
                city: {
                    city_id: 1,
                    city_name: "Hyderabad"
                },
                schedule_screen_id: 32,
                screen_name: "test device",
                screen_size: 24,
                groups: [
                {
                    group_name: "Group 1",
                    group_id: 1,
                    group_screen_id: 4
                }
                ],
                address: "mount fort",
                resolution: "1024*768",
                screen_id: 2
            }
            ],
            schedule_title: "11"
        }
    ]
    """
    debugFileLog.info("inside get_schedules")
    user_details = get_userdetails(request)
    user_schedules = Schedule.get_user_relevant_objects(user_details)
    json_data = default_schedule_serializer(querySet=user_schedules)
    return obj_to_json_response(json_data)


@transaction.atomic
@login_required
def delete_schedule(request):
    debugFileLog.info("inside delete schedule")
    user_details = get_userdetails(request)
    errors = []
    try:
        with transaction.atomic():
            posted_data = string_to_dict(request.body)
            schedule_id = int(posted_data.get('schedule_id'))
            schedule = Schedule.get_user_relevant_objects(user_details=user_details).get(schedule_id=schedule_id)
            # Cascading delete would delete all the schedule screens
            schedule.delete()
            success = True
    except Exception as e:
        success = False
        errors = ['Sorry, you do not have access to this schedule or something wrong has happened']
        debugFileLog.exception(errors[0])
        mail_exception(exception=e)
    return ajax_response(success=success, errors=errors)


def calendar_schedules(start_datetime, end_datetime, screen_id=None, group_id=None):
    if screen_id and group_id:
        schedule_id_list = ScheduleScreens.objects.filter(screen_id=screen_id, group_id=group_id).values_list(
            'schedule_id', flat=True).distinct()
    elif screen_id:
        # Show the schedules of the screen as well as the schedule of the group in which screen lies.
        schedule_id_list = ScheduleScreens.objects.filter(screen_id=screen_id).values_list('schedule_id',
                                                                                           flat=True).distinct()
    elif group_id:
        schedule_id_list = ScheduleScreens.objects.filter(screen__isnull=True, group_id=group_id).values_list(
            'schedule_id', flat=True).distinct()
    else:
        return []
    schedule_panes = SchedulePane.objects.filter(schedule_id__in=schedule_id_list)
    screen_data_json = []
    for each_schedule_pane in schedule_panes:
        if each_schedule_pane.event:
            occurrences = each_schedule_pane.event.get_occurrences(start_datetime, end_datetime)
            if not occurrences:
                continue
            schedule = each_schedule_pane.schedule
            schedule_json = default_schedule_serializer([schedule])
            if group_id:
                display_type = 'special'
            else:
                display_type = 'info'
            title = schedule.schedule_title
            title = title + ' - ' + schedule.layout.title if schedule.layout else title
            title = title + ' - ' + each_schedule_pane.layout_pane.title if each_schedule_pane.layout_pane else title
            for each_occur in occurrences:
                campaign_dict = {'title': title,
                                 'startsAt': get_ist_datetime(each_occur.start),
                                 'endsAt': get_ist_datetime(each_occur.end),
                                 'schedule': schedule_json[0],
                                 # some default values
                                 'type': display_type,
                                 'editable': True,
                                 'deletable': True,
                                 }
                screen_data_json.append(campaign_dict)
    return screen_data_json


def get_calendar_events(params):
    try:
        screen_id = params.get('screen_id')
        group_id = params.get('group_id')
        if screen_id:
            screen_id = int(screen_id)
        if group_id:
            group_id = int(group_id)
        month = params.get('month')
        if month:
            month = int(month)
        else:
            month = timezone.now().month
        year = timezone.now().year
        (_,days_in_month) = calendar.monthrange(year, month)
        screen_data = []
        for day in range(days_in_month):
            start_datetime = datetime.datetime(year=year, month=month, day=day+1)
            end_datetime = start_datetime.replace(hour=23, minute=59, second=59)
            day_schedules = calendar_schedules(start_datetime=get_utc_datetime(start_datetime),
                                               end_datetime=get_utc_datetime(end_datetime), screen_id=screen_id,
                                               group_id=group_id)
            screen_data.extend(day_schedules)
    except Exception as e:
        screen_data = []
        mail_exception(exception=e)
    return obj_to_json_response(screen_data)


def get_screen_events(request):
    params = request.GET
    return get_calendar_events(params)


def get_group_events(request):
    params = request.GET
    return get_calendar_events(params)
