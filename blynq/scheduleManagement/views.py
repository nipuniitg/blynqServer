import datetime
import calendar

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedule.models import Event, Rule
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# Create your views here.
# from schedule.views import calendar
from authentication.models import LocalServer, Organization
from contentManagement.models import Content
from contentManagement.serializers import ContentSerializer
from customLibrary.views_lib import get_userdetails, ajax_response, obj_to_json_response, string_to_dict, list_to_comma_string, \
    default_string_to_datetime, generate_utc_datetime, debugFileLog, get_ist_datetime, get_utc_datetime
from playlistManagement.models import Playlist, PlaylistItems
from playlistManagement.serializers import PlaylistSerializer
from scheduleManagement.models import Schedule, ScheduleScreens, SchedulePlaylists
from scheduleManagement.serializers import ScheduleSerializer
from screenManagement.models import Screen, Group, ScreenActivationKey
from screenManagement.views import debugFileLog


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
        weekday_string = list_to_comma_string(bylistday)
        return key_str + ':' + weekday_string
    return ''


def append_params(params, new_keyvalue):
    return params + ';' + new_keyvalue


# byweekday should be a list [0,2,3] meaning 0-Monday, 1-Tuesday, 2-Wednesday, 3-Thursday, 4-Friday, 5-Saturday,6-Sunday
def generate_rule_params(interval=1, bymonthday=None, byweekday=None, byweekno=None):
    debugFileLog.info("inside generate_rule_params")
    params = interval_param(interval)
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='bymonthday', bylistday=bymonthday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekno', bylistday=byweekno))
    return params


def upsert_schedule_screens(user_details, schedule, schedule_screens, event_dict):
    debugFileLog.info("inside upsert_schedule_screens")
    error = ''
    schedule_screen_id_list = []
    for item in schedule_screens:
        schedule_screen_id = int(item.get('schedule_screen_id'))
        if schedule_screen_id == -1:
            screen_id = int(item.get('screen_id'))
            screen = Screen.get_user_relevant_objects(user_details).get(screen_id=screen_id)
            event = Event(**event_dict)
            event.calendar = screen.screen_calendar
            event.save()
            entry = ScheduleScreens.objects.create(screen=screen, schedule=schedule, event=event)
            schedule_screen_id = entry.schedule_screen_id
        else:
            entry = ScheduleScreens.objects.get(schedule_screen_id=schedule_screen_id)
            events = Event.objects.filter(id=entry.event.id)
            # Not deleting the rule as all the events have the same rule
            # for event in events:
            #     if event.rule:
            #         rule = event.rule
            #         event.rule = None
            #         event.save()
            #         rule.delete()
            events.update(**event_dict)
            entry.save()
        schedule_screen_id_list.append(schedule_screen_id)

    # Remove screens not in the schedule
    removed_schedule_screens = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=True).exclude(
        schedule_screen_id__in=schedule_screen_id_list)
    if removed_schedule_screens:
        removed_schedule_screens.delete()
    success = True
    return success, error


def upsert_schedule_groups(user_details, schedule, schedule_groups, event_dict):
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
            event = Event(**event_dict)
            event.save()
            entry = ScheduleScreens(schedule=schedule, group=group, event=event)
            entry.save()
            schedule_screen_id_list.append(entry.schedule_screen_id)
            for screen in group.screen_set.all():
                screen_event = Event(**event_dict)
                screen_event.calendar = screen.screen_calendar
                screen_event.save()
                entry = ScheduleScreens(screen=screen, schedule=schedule, group=group, event=screen_event)
                entry.save()
                schedule_screen_id_list.append(entry.schedule_screen_id)
        else:
            entry = ScheduleScreens.objects.get(schedule_screen_id=schedule_screen_id)
            events = Event.objects.filter(id=entry.event.id)
            # Not deleting the rule as all the events have the same rule
            # for event in events:
            #     if event.rule:
            #         rule = event.rule
            #         event.rule = None
            #         event.save()
            #         rule.delete()
            events.update(**event_dict)
            entry.save()
            schedule_screen_id_list.append(schedule_screen_id)

    # Remove groups not in the schedule
    removed_schedule_groups = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=False).exclude(
        schedule_screen_id__in=schedule_screen_id_list)
    if removed_schedule_groups:
        removed_schedule_groups.delete()
    success = True
    return success, error


# upsert schedule playlists
def upsert_schedule_playlists(user_details, schedule, schedule_playlists):
    debugFileLog.info("inside upsert_schedule_playlists")
    error = ''
    schedule_playlist_id_list = []
    for pos_index, item in enumerate(schedule_playlists):
        schedule_playlist_id = int(item.get('schedule_playlist_id'))
        playlist_id = int(item.get('playlist_id'))
        playlist = Playlist.get_user_relevant_objects(user_details).get(playlist_id=playlist_id)
        if schedule_playlist_id == -1:
            entry = SchedulePlaylists.objects.create(schedule=schedule, playlist=playlist, position_index=pos_index)
            schedule_playlist_id = entry.schedule_playlist_id
        else:
            entry = SchedulePlaylists.objects.get(schedule_playlist_id=schedule_playlist_id)
            entry.position_index = pos_index
            entry.save()
        schedule_playlist_id_list.append(schedule_playlist_id)

    # Remove playlists not in playlist_schedules
    removed_playlist_schedules = SchedulePlaylists.objects.filter(schedule=schedule).exclude(
        schedule_playlist_id__in=schedule_playlist_id_list)
    for playlist_schedule in removed_playlist_schedules:
        playlist_schedule.delete()
    success = True
    return success, error


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
    start = timezone.now().replace(hour=0, minute=0, second=0)
    end = timezone.now().replace(hour=23, minute=59, second=59)
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
            schedule_playlists = posted_data.get('schedule_playlists')
            schedule_screens = posted_data.get('schedule_screens')
            schedule_groups = posted_data.get('schedule_groups')
            timeline = posted_data.get('timeline')
            user_schedules = Schedule.get_user_relevant_objects(user_details=user_details)

            # upsert schedule
            if schedule_id == -1:
                schedule = Schedule(schedule_title=schedule_title, created_by=user_details,
                                    last_updated_by=user_details, organization=user_details.organization)
            else:
                schedule = user_schedules.get(schedule_id=schedule_id)
                schedule.schedule_title = schedule_title
                schedule.last_updated_by = user_details
            schedule.save()

            success, error = upsert_schedule_playlists(user_details=user_details, schedule=schedule,
                                                       schedule_playlists=schedule_playlists)
            errors.append(error)

            # Upsert Groups and Screens in a schedule
            event_dict = event_dict_from_timeline(timeline, schedule)
            success_screens, error = upsert_schedule_screens(user_details=user_details, schedule=schedule,
                                                             schedule_screens=schedule_screens, event_dict=event_dict)
            success = success and success_screens
            errors.append(error)

            success_groups, error = upsert_schedule_groups(user_details=user_details, schedule=schedule,
                                                           schedule_groups=schedule_groups, event_dict=event_dict)
            success = success and success_groups
            errors.append(error)
    except Exception as e:
        success = False
        error = 'Error while upserting content to schedule'
        debugFileLog.exception(error)
        debugFileLog.exception(e)
        errors.append(error)
    return ajax_response(success=success, errors=errors)


@csrf_exempt
def device_key_active(request):
    """
    :param request:
    :return: Json dict of success and error, success will be True if the activation_key sent in the post request
     is not in_use and verified.
     If the activation_key is not in the database, then adding it here and manually check the verified through the
     admin portal
    """
    success = False
    error = ''
    posted_data = string_to_dict(request.body)
    activation_key = posted_data.get('device_key')
    if not activation_key:
        error = 'Activation key not found'
        return ajax_response(success=success, errors=error)
    try:
        screen_activation_key = ScreenActivationKey.objects.get(activation_key=activation_key)
        if not screen_activation_key.verified:
            error = 'New device with device key %s is asking for activation. ' % activation_key
            error += 'Check the verified boolean if the device is valid.'
            debugFileLog.warning(error)
            # elif screen_activation_key.in_use:
            #     error = 'Device activation key %s is already in use.' % activation_key
            #     debugFileLog.warning(error)
        else:
            success = True
    except ScreenActivationKey.DoesNotExist:
        error = 'Activation key %s doesn\'t exist in the database.\n ' % activation_key
        error += 'Adding it, check the verified boolean if the device is valid.\n'
        debugFileLog.warning(error)
        try:
            screen_activation_key = ScreenActivationKey(activation_key=activation_key)
            screen_activation_key.save()
        except Exception as e:
            db_error = 'Adding the above activation_key to the database failed with the exception {0} \n'.format(str(e))
            debugFileLog.error(db_error)
        success = False
    return ajax_response(success=success, errors=error)


@csrf_exempt
def get_screen_data(request, nof_days=7):
    debugFileLog.info("inside get_screen_data")
    # user_details, organization = user_and_organization(request)
    errors = []
    screen_data_json = []
    success = False
    is_modified = False
    posted_data = string_to_dict(request.body)
    # the datetime format of last_received should be
    last_received = posted_data.get('last_received')
    unique_device_key = posted_data.get('device_key')
    last_received_datetime = default_string_to_datetime(last_received)
    last_received_date = last_received_datetime.date()
    try:
        # screen = Screen.objects.get(screen_id=screen_id)
        screen = ScreenActivationKey.objects.get(activation_key=unique_device_key, in_use=True).screen
        calendar = screen.screen_calendar
        if calendar:
            current_datetime = timezone.now()
            calendar_events = calendar.events.exclude(end_recurring_period__lt=current_datetime)
            start_time = current_datetime.replace(hour=0, minute=0, second=0)
            time_diff = datetime.timedelta(days=nof_days)
            end_time = start_time + time_diff
            if not calendar_events:
                is_modified = True
            schedule_for_event = False
            for event in calendar_events:
                try:
                    # Each event should have only one entry in Schedule_Screens
                    screen_schedule = event.schedulescreens
                    schedule_for_event = True
                except Exception as e:
                    debugFileLog.exception('Event does not exist in the schedule screens')
                    debugFileLog.exception(e)
                    continue
                schedule = screen_schedule.schedule
                if schedule.last_updated_time > last_received_datetime:
                    is_modified = True
                    break
                elif last_received_date == current_datetime.date():
                    is_modified = False
                else:
                    next_day_after_week = last_received_datetime.replace(hour=0, minute=0, second=0) + \
                                          datetime.timedelta(days=nof_days)
                    # The player keeps the data of nof_days=7, so if there is no change in the schedules after the
                    # last_received_datetime and no occurences on the 8th day
                    occurrences = event.get_occurrences(next_day_after_week, end_time)
                    if occurrences:
                        is_modified = True
                        break
            completed_schedules = []
            if is_modified:
                for event in calendar_events:
                    try:
                        # Each event should have only one entry in Schedule_Screens
                        screen_schedule = event.schedulescreens
                        schedule_for_event = True
                    except Exception as e:
                        debugFileLog.exception('Event does not exist in the schedule screens')
                        debugFileLog.exception(e)
                        continue
                    schedule = screen_schedule.schedule
                    if schedule.schedule_id in completed_schedules:
                        continue
                    else:
                        completed_schedules.append(schedule.schedule_id)
                    occurrences = event.get_occurrences(start_time, end_time)
                    if not occurrences:
                        continue
                    playlists = schedule.playlists.all()
                    playlists_json = PlaylistSerializer().serialize(playlists, fields=('playlist_id', 'playlist_title',
                                                                                       'playlist_items'))
                    for each_occur in occurrences:
                        campaign_dict = {'schedule_id': screen_schedule.schedule.schedule_id,
                                         'playlists': playlists_json,
                                         'last_updated_time': schedule.last_updated_time,
                                         'start_time': each_occur.start,
                                         'end_time': each_occur.end}
                        screen_data_json.append(campaign_dict)
            if not schedule_for_event:
                is_modified = True
        else:
            is_modified = True
        campaigns_json = {'campaigns': screen_data_json, 'is_modified': is_modified}
        success = True
        return obj_to_json_response(campaigns_json)
    except Exception as e:
        errors = "Error while fetching the occurences or invalid screen identifier"
        debugFileLog.exception(errors)
        debugFileLog.exception(e)
    return ajax_response(success=success, errors=errors)


@csrf_exempt
def get_content_urls_local(request, nof_days=1):
    """
    :param request:
    :param nof_days:
    :return:
    returns a list of urls for the content in the playlists scheduled for the next day
    """
    posted_data = string_to_dict(request.body)
    unique_key = posted_data.get('unique_key')
    try:
        local_server = LocalServer.objects.get(unique_key=unique_key)
        organization = local_server.organization
        screens = Screen.objects.filter(owned_by=organization)
        schedule_screens = ScheduleScreens.objects.filter(screen__in=screens)
        current_datetime = timezone.now()
        next_day = current_datetime + datetime.timedelta(days=1)
        start_time = next_day.replace(hour=0, minute=0, second=0)
        time_diff = datetime.timedelta(days=nof_days)
        end_time = start_time + time_diff
        required_schedule_ids = []
        for schedule_screen in schedule_screens:
            if schedule_screen.event:
                occurrences = schedule_screen.event.get_occurrences(start_time, end_time)
                if occurrences:
                    required_schedule_ids.append(schedule_screen.schedule_id)
        playlist_ids = SchedulePlaylists.objects.filter(schedule_id__in=required_schedule_ids).values_list(
            'playlist_id', flat=True)
        content_ids = PlaylistItems.objects.filter(playlist_id__in=playlist_ids).values_list('content_id', flat=True)
        contents = Content.objects.filter(content_id__in=content_ids).exclude(content_type__file_type__contains='web')
        json_data = ContentSerializer().serialize(contents, fields='document')
        url_list = [str(element['url']) for element in json_data]
        json_obj = dict()
        json_obj['urls'] = url_list
        json_obj['success'] = True
        return obj_to_json_response(json_obj)
    except Exception as e:
        debugFileLog.exception(e)
        success=False
        errors = str(e)
        return ajax_response(success=success, errors=errors)


def default_schedule_serializer(querySet):
    return ScheduleSerializer().serialize(querySet, fields=('schedule_id', 'schedule_title',
                                                            'schedule_playlists', 'timeline',
                                                            'schedule_screens', 'schedule_groups'))


def get_screen_schedules(request, screen_id):
    debugFileLog.info("inside get_screen_schedules")
    screen_id = int(screen_id)
    user_details = get_userdetails(request)
    screen_schedule_id_list = ScheduleScreens.objects.filter(screen_id=screen_id).values_list(
        'schedule_id', flat=True).distinct()
    screen_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=screen_schedule_id_list)
    json_data = default_schedule_serializer(querySet=screen_schedules)
    return obj_to_json_response(json_data)


def get_group_schedules(request, group_id):
    debugFileLog.info("inside get_group_schedules")
    screen_id = int(group_id)
    user_details = get_userdetails(request)
    group_schedule_id_list = ScheduleScreens.objects.filter(group_id=group_id).values_list(
        'schedule_id', flat=True).distinct()
    screen_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=group_schedule_id_list)
    json_data = default_schedule_serializer(querySet=screen_schedules)
    return obj_to_json_response(json_data)


def get_playlist_schedules(request, playlist_id):
    debugFileLog.info("inside get_playlist_schedules")
    playlist_id = int(playlist_id)
    user_details = get_userdetails(request)
    playlist_schedule_id_list = SchedulePlaylists.objects.filter(playlist_id=playlist_id).values_list(
        'schedule_id', flat=True).distinct()
    playlist_schedules = Schedule.get_user_relevant_objects(user_details=user_details).filter(
        schedule_id__in=playlist_schedule_id_list)
    json_data = default_schedule_serializer(querySet=playlist_schedules)
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
    success = False
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
        errors = ['Sorry, you do not have access to this schedule']
        debugFileLog.exception(errors[0])
        debugFileLog.exception(e)
    return ajax_response(success=success, errors=errors)


def calendar_schedules(start_datetime, end_datetime, screen_id=None, group_id=None):
    if screen_id and group_id:
        schedule_screens = ScheduleScreens.objects.filter(screen_id=screen_id, group_id=group_id)
    elif screen_id:
        schedule_screens = ScheduleScreens.objects.filter(screen_id=screen_id)
    elif group_id:
        schedule_screens = ScheduleScreens.objects.filter(group_id=group_id)
    else:
        return []
    screen_data_json = []
    for each_schedule_screen in schedule_screens:
        if each_schedule_screen.event:
            occurrences = each_schedule_screen.event.get_occurrences(start_datetime, end_datetime)
            if not occurrences:
                continue
            schedule = each_schedule_screen.schedule
            schedule_json = default_schedule_serializer([schedule])
            for each_occur in occurrences:
                campaign_dict = {'title': schedule.schedule_title,
                                 'startsAt': get_ist_datetime(each_occur.start),
                                 'endsAt': get_ist_datetime(each_occur.end),
                                 'schedule': schedule_json[0],
                                 # some default values
                                 'type': 'info',
                                 'editable': True,
                                 'deletable': True,
                                 }
                screen_data_json.append(campaign_dict)
    return screen_data_json


def get_calendar_events(params):
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
    return obj_to_json_response(screen_data)


def get_screen_events(request):
    params = request.GET
    return get_calendar_events(params)


def get_group_events(request):
    params = request.GET
    return get_calendar_events(params)