import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from schedule.models import Event, Rule
# Create your views here.
# from schedule.views import calendar
from customLibrary.views_lib import get_userdetails, ajax_response, obj_to_json_response, string_to_dict, \
    list_to_comma_string, generate_utc_datetime, get_ist_datetime, get_utc_datetime, debugFileLog
from playlistManagement.models import Playlist
from scheduleManagement.models import Schedule, SchedulePlaylists, ScheduleScreens, SchedulePane
from scheduleManagement.serializers import default_schedule_serializer
from screenManagement.models import Screen, Group
from layoutManagement.models import Layout


@login_required
def index(request):
    return render(request, 'scheduleManagement/schedule_index.html')


def add_schedule(request):
    return render(request, 'scheduleManagement/schedule_details.html')


def interval_param(interval):
    debugFileLog.info('inside interval_param')
    return 'interval:' + str(interval)


def list_to_param(key_str, bylistday):
    if bylistday:
        try:
            weekday_string = list_to_comma_string(bylistday)
            return key_str + ':' + weekday_string
        except Exception as e:
            debugFileLog.exception(e)
    return ''


def append_params(params, new_keyvalue):
    if new_keyvalue:
        return params + ';' + new_keyvalue
    else:
        return params


# byweekday should be a list [0,2,3] meaning 0-Monday, 1-Tuesday, 2-Wednesday, 3-Thursday, 4-Friday, 5-Saturday,6-Sunday
def generate_rule_params(interval=1, bymonthday=None, byweekday=None, byweekno=None):
    debugFileLog.info("inside generate_rule_params")
    params = interval_param(interval)
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='bymonthday', bylistday=bymonthday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekno', bylistday=byweekno))
    return params


def generate_rule(timeline, name, description):
    debugFileLog.info("inside generate_rule")
    interval = int(timeline.get('interval'))
    byweekno = timeline.get('byweekno')
    bymonthday = timeline.get('bymonthday')
    byweekday = timeline.get('byweekday')
    frequency = timeline.get('frequency')
    if not frequency:
        frequency = 'DAILY'
    params = generate_rule_params(interval=interval, bymonthday=bymonthday, byweekday=byweekday, byweekno=byweekno)
    rule = Rule(name=name, description=description, frequency=frequency, params=params)
    rule.save()
    return rule


def event_for_allday(schedule, timeline):
    debugFileLog.info("inside event_for_allday")
    start_date = timeline.get('start_date')
    start_time = "00:00"  # datetime.time(0)
    start = generate_utc_datetime(ist_date=start_date, ist_time=start_time)
    end_date = start_date
    end_time = "23:59"  # datetime.time(23, 59, 59, 999)
    end = generate_utc_datetime(ist_date=end_date, ist_time=end_time)
    end_recurring_period_date = timeline.get('end_recurring_period')
    end_recurring_period = generate_utc_datetime(ist_date=end_recurring_period_date, ist_time=end_time)
    rule = generate_rule(timeline=timeline, name=schedule.schedule_title, description=schedule.schedule_title)
    creator = schedule.created_by.user if schedule.created_by else None
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                  'rule': rule, 'end_recurring_period': end_recurring_period}
    return event_dict


def event_for_always(schedule):
    debugFileLog.info("inside event_for_always")
    ist_now = get_ist_datetime(timezone.now())
    ist_start = ist_now.replace(hour=0, minute=0, second=0)
    ist_end = ist_now.replace(hour=23, minute=59, second=59)
    start = get_utc_datetime(ist_start)
    end = get_utc_datetime(ist_end)
    rule = Rule(name=schedule.schedule_title, description=schedule.schedule_title, frequency='DAILY')
    rule.save()
    creator = schedule.created_by.user if schedule.created_by else None
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                  'rule': rule, 'end_recurring_period': None}
    return event_dict


def event_dict_from_timeline(timeline, schedule):
    debugFileLog.info("insisde event_dict_from_timeline")
    is_always = timeline.get('is_always')
    all_day = timeline.get('all_day')
    recurrence_absolute = timeline.get('recurrence_absolute')
    if is_always is not None:
        schedule.is_always = is_always
    if all_day is not None:
        schedule.all_day = all_day
    if recurrence_absolute is not None:
        schedule.recurrence_absolute = recurrence_absolute
    schedule.save()
    if is_always:
        return event_for_always(schedule)
    elif all_day:
        return event_for_allday(schedule, timeline)
    else:
        start_date = timeline.get('start_date')
        start_time = timeline.get('start_time')
        start = generate_utc_datetime(ist_date=start_date, ist_time=start_time)
        end_date = start_date
        end_time = timeline.get('end_time')
        end = generate_utc_datetime(ist_date=end_date, ist_time=end_time)
        end_recurring_period_time = end_time
        end_recurring_period = timeline.get('end_recurring_period')
        end_recurring_period = generate_utc_datetime(ist_date=end_recurring_period, ist_time=end_recurring_period_time)
        rule = generate_rule(timeline, name=schedule.schedule_title, description=schedule.schedule_title)
        creator = schedule.created_by.user if schedule.created_by else None
        event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                      'rule': rule, 'end_recurring_period': end_recurring_period}
        return event_dict


def upsert_schedule_screens(user_details, schedule, schedule_screens):
    debugFileLog.info("inside upsert_schedule_screens")
    error = ''
    schedule_screen_id_list = []
    for item in schedule_screens:
        schedule_screen_id = int(item.get('schedule_screen_id'))
        if schedule_screen_id == -1:
            screen_id = int(item.get('screen_id'))
            screen = Screen.get_user_relevant_objects(user_details).get(screen_id=screen_id)
            # event = Event(**event_dict)
            # event.calendar = screen.screen_calendar
            # event.save()
            entry = ScheduleScreens.objects.create(screen=screen, schedule=schedule)
            schedule_screen_id = entry.schedule_screen_id
        # else:
            # entry = ScheduleScreens.objects.get(schedule_screen_id=schedule_screen_id)
            # events = Event.objects.filter(id=entry.event.id)
            # # Not deleting the rule as all the events have the same rule
            # # for event in events:
            # #     if event.rule:
            # #         rule = event.rule
            # #         event.rule = None
            # #         event.save()
            # #         rule.delete()
            # events.update(**event_dict)
            # entry.save()
        schedule_screen_id_list.append(schedule_screen_id)

    # Remove screens not in the schedule
    removed_schedule_screens = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=True).exclude(
        schedule_screen_id__in=schedule_screen_id_list)
    # Send a push message to all the screens which are removed from the schedule
    for deleted_screen in removed_schedule_screens:
        from playerManagement.views import notify_player
        notify_player(deleted_screen.screen)
    if removed_schedule_screens:
        removed_schedule_screens.delete()
    success = True
    return success, error


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
            # schedule_screen_id_list.append(entry.schedule_screen_id)
            for screen in group.screen_set.all():
                # screen_event = Event(**event_dict)
                # screen_event.calendar = screen.screen_calendar
                # screen_event.save()
                entry = ScheduleScreens(screen=screen, schedule=schedule, group=group)
                entry.save()
                schedule_screen_id_list.append(entry.schedule_screen_id)
        schedule_screen_id_list.append(schedule_screen_id)

    # Remove groups not in the schedule
    removed_schedule_groups = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=False).exclude(
        schedule_screen_id__in=schedule_screen_id_list)
    # Send a push message to all the screens which are removed from the schedule
    for deleted_screen in removed_schedule_groups:
        from playerManagement.views import notify_player
        notify_player(deleted_screen.screen)
    if removed_schedule_groups:
        removed_schedule_groups.delete()
    success = True
    return success, error


# upsert schedule playlists
def upsert_schedule_playlists(user_details, schedule_pane_id, schedule_playlists):
    debugFileLog.info("inside upsert_schedule_playlists")
    error = ''
    schedule_playlist_id_list = []
    for pos_index, item in enumerate(schedule_playlists):
        schedule_playlist_id = int(item.get('schedule_playlist_id'))
        playlist_id = int(item.get('playlist_id'))
        playlist = Playlist.get_user_relevant_objects(user_details).get(playlist_id=playlist_id)
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
    if removed_playlist_schedules:
        removed_playlist_schedules.delete()
    return True, error


def upsert_schedule_panes(user_details, schedule, schedule_panes, layout):
    debugFileLog.info("inside upsert_schedule_panes")
    error = ''
    schedule_pane_id_list = []
    for item in schedule_panes:
        schedule_pane_id = int(item.get('schedule_pane_id'))
        schedule_playlists = item.get('schedule_playlists')
        layout_pane = item.get('layout_pane')
        layout_pane_id = int(layout_pane.get('layout_pane_id'))
        timeline = item.get('timeline')
        is_always = timeline.get('is_always')
        all_day = timeline.get('all_day')
        recurrence_absolute = timeline.get('recurrence_absolute')
        if not recurrence_absolute:
            recurrence_absolute = False
        if schedule_playlists:
            event_dict = event_dict_from_timeline(timeline=timeline, schedule=schedule)
            event = Event(**event_dict)
            event.save()
        else:
            event = None
        if schedule_pane_id == -1:
            schedule_pane = SchedulePane(schedule=schedule, layout_pane_id=layout_pane_id,
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
    if remove_schedule_panes:
        remove_schedule_panes.delete()
    return True, error


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
            schedule_screens = posted_data.get('schedule_screens')
            schedule_groups = posted_data.get('schedule_groups')
            is_split = posted_data.get('is_split')
            layout = posted_data.get('layout')
            schedule_panes = posted_data.get('schedule_panes')
            user_schedules = Schedule.get_user_relevant_objects(user_details=user_details)
            layout_id = int(layout.get('layout_id'))
            layout = Layout.objects.get(layout_id=layout_id)
            # upsert schedule
            if schedule_id == -1:
                schedule = Schedule(schedule_title=schedule_title, created_by=user_details, is_split=is_split,
                                    layout=layout, last_updated_by=user_details,
                                    organization=user_details.organization)
            else:
                schedule = user_schedules.get(schedule_id=schedule_id)
                schedule.schedule_title = schedule_title
                schedule.is_split = is_split
                schedule.layout = layout
                schedule.last_updated_by = user_details
            schedule.save()

            success_screens, error = upsert_schedule_screens(user_details=user_details, schedule=schedule,
                                                             schedule_screens=schedule_screens)
            errors.append(error)

            success_groups, error = upsert_schedule_groups(user_details=user_details, schedule=schedule,
                                                           schedule_groups=schedule_groups)
            errors.append(error)

            success_panes, error = upsert_schedule_panes(user_details=user_details, schedule=schedule,
                                                         schedule_panes=schedule_panes, layout=layout)
            success = success_screens and success_groups and success_panes
            errors.append(error)
    except Exception as e:
        success = False
        error = 'Error while upserting content to schedule'
        debugFileLog.exception(error)
        debugFileLog.exception(e)
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
    group_schedule_id_list = ScheduleScreens.objects.filter(schedule__deleted=False, screen__isnull=True,
                                                            group_id=group_id).values_list(
        'schedule_id', flat=True).distinct()
    group_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=group_schedule_id_list)
    json_data = default_schedule_serializer(querySet=group_schedules)
    return obj_to_json_response(json_data)


# def get_playlist_schedules(request, playlist_id):
#     debugFileLog.info("inside get_playlist_schedules")
#     playlist_id = int(playlist_id)
#     user_details = get_userdetails(request)
#     playlist_schedule_pane_id_list = SchedulePlaylists.objects.filter(playlist_id=playlist_id).values_list(
#         'schedule_pane_id', flat=True).distinct()
#     playlist_schedules = Schedule.get_user_relevant_objects(user_details=user_details).filter(
#         schedule_pane_id__in=playlist_schedule_pane_id_list)
#     json_data = default_schedule_serializer(querySet=playlist_schedules)
#     return obj_to_json_response(json_data)


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
            # schedule.delete()
            schedule.deleted = True
            schedule.save()
            success = True
    except Exception as e:
        success = False
        errors = ['Sorry, you do not have access to this schedule']
        debugFileLog.exception(errors[0])
        debugFileLog.exception(e)
    return ajax_response(success=success, errors=errors)


def calendar_schedules(start_datetime, end_datetime, screen_id=None, group_id=None):
    if screen_id and group_id:
        schedule_id_list = ScheduleScreens.objects.filter(schedule__deleted=False, screen_id=screen_id,
                                                          group_id=group_id).values_list(
            'schedule_id', flat=True).distinct()
    elif screen_id:
        # Show the schedules of the screen as well as the schedule of the group in which screen lies.
        schedule_id_list = ScheduleScreens.objects.filter(schedule__deleted=False, screen_id=screen_id).values_list(
            'schedule_id', flat=True).distinct()
    elif group_id:
        schedule_id_list = ScheduleScreens.objects.filter(schedule__deleted=False, screen__isnull=True,
                                                          group_id=group_id).values_list(
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
        debugFileLog.exception(e)
    return obj_to_json_response(screen_data)


def get_screen_events(request):
    params = request.GET
    return get_calendar_events(params)


def get_group_events(request):
    params = request.GET
    return get_calendar_events(params)
