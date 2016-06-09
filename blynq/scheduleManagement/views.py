import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedule.models import Event, Rule
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# Create your views here.
# from schedule.views import calendar

from customLibrary.views_lib import get_userdetails, ajax_response, obj_to_json_response, string_to_dict, list_to_comma_string, \
    default_string_to_datetime, get_utc_datetime, debugFileLog
from playlistManagement.models import Playlist
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


def default_rule(frequency='DAILY'):
    if frequency == 'DAILY':
        return Rule.objects.filter(name='default-daily')[0]
    elif frequency == 'WEEKLY':
        return Rule.objects.filter(name='default-weekly')[0]
    elif frequency == 'MONTHLY':
        return Rule.objects.filter(name='default-monthly')[0]
    elif frequency == 'YEARLY':
        return Rule.objects.filter(name='default-yearly')[0]


def interval_param(interval):
    print 'inside interval_param'
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
    print "inside generate_rule_params"
    params = interval_param(interval)
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='bymonthday', bylistday=bymonthday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekno', bylistday=byweekno))
    return params


def upsert_schedule_screens(user_details, schedule, schedule_screens, event_dict):
    print "inside upsert_schedule_screens"
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
            for event in events:
                if event.rule:
                    rule = event.rule
                    event.rule = None
                    event.save()
                    rule.delete()
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
    print "inside upsert_schedule_groups"
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
            for event in events:
                if event.rule:
                    rule = event.rule
                    event.rule = None
                    event.save()
                    rule.delete()
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
    print "inside upsert_schedule_playlists"
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
    print "inside generate_rule"
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
    print "inside event_for_allday"
    start_date = timeline.get('start_date')
    start_time = "00:00"  # datetime.time(0)
    start = get_utc_datetime(ist_date=start_date, ist_time=start_time)
    end_date = start_date
    end_time = "23:59"  # datetime.time(23, 59, 59, 999)
    end = get_utc_datetime(ist_date=end_date, ist_time=end_time)
    end_recurring_period_date = timeline.get('end_recurring_period')
    end_recurring_period = get_utc_datetime(ist_date=end_recurring_period_date, ist_time=end_time)
    rule = generate_rule(timeline=timeline, name=schedule.schedule_title, description=schedule.schedule_title)
    creator = schedule.created_by.user if schedule.created_by else None
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                  'rule': rule, 'end_recurring_period': end_recurring_period}
    return event_dict


def event_for_always(schedule):
    print "inside event_for_always"
    start = timezone.now().replace(hour=0, minute=0, second=0)
    end = timezone.now().replace(hour=23, minute=59, second=59)
    rule = Rule(name=schedule.schedule_title, description=schedule.schedule_title, frequency='DAILY')
    rule.save()
    creator = schedule.created_by.user if schedule.created_by else None
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                  'rule': rule, 'end_recurring_period': None}
    return event_dict


def event_dict_from_timeline(timeline, schedule):
    print "insisde event_dict_from_timeline"
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
        start = get_utc_datetime(ist_date=start_date, ist_time=start_time)
        end_date = start_date
        end_time = timeline.get('end_time')
        end = get_utc_datetime(ist_date=end_date, ist_time=end_time)
        end_recurring_period_time = end_time
        end_recurring_period = timeline.get('end_recurring_period')
        end_recurring_period = get_utc_datetime(ist_date=end_recurring_period, ist_time=end_recurring_period_time)
        rule = generate_rule(timeline, name=schedule.schedule_title, description=schedule.schedule_title)
        creator = schedule.created_by.user if schedule.created_by else None
        event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': creator,
                      'rule': rule, 'end_recurring_period': end_recurring_period}
        return event_dict


@transaction.atomic
@login_required
def upsert_schedule(request):
    print "inside upsert_schedule"
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
        print "Exception is ", e
        error = 'Error while upserting content to schedule'
        errors.append(error)
        print errors
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
    print "inside get_screen_data"
    # user_details, organization = user_and_organization(request)
    errors = []
    screen_data_json = []
    success = False
    is_modified = False
    posted_data = string_to_dict(request.body)
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
                    print "Exception is ", e
                    print 'Event does not exist in the schedule screens'
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
                        print "Exception is ", e
                        print 'Event does not exist in the schedule screens'
                        continue
                    schedule = screen_schedule.schedule
                    if schedule.schedule_id in completed_schedules:
                        continue
                    else:
                        completed_schedules.append(schedule.schedule_id)
                    occurrences = event.get_occurrences(start_time, end_time)
                    if not occurrences:
                        continue
                    # TODO: optimize this
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
        print "Exception is ", e
        errors = "Error while fetching the occurences or invalid screen identifier"
        print errors
    return ajax_response(success=success, errors=errors)


def get_screen_schedules(request, screen_id):
    print "inside get_screen_schedules"
    screen_id = int(screen_id)
    user_details = get_userdetails(request)
    screen_schedule_id_list = ScheduleScreens.objects.filter(screen_id=screen_id).values_list(
        'schedule_id', flat=True).distinct()
    screen_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=screen_schedule_id_list)
    json_data = ScheduleSerializer().serialize(screen_schedules, fields=('schedule_id', 'schedule_title',
                                                                         'schedule_playlists', 'timeline',
                                                                         'schedule_screens', 'schedule_groups'))
    return obj_to_json_response(json_data)


def get_group_schedules(request, group_id):
    print "inside get_group_schedules"
    screen_id = int(group_id)
    user_details = get_userdetails(request)
    group_schedule_id_list = ScheduleScreens.objects.filter(group_id=group_id).values_list(
        'schedule_id', flat=True).distinct()
    screen_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=group_schedule_id_list)
    json_data = ScheduleSerializer().serialize(screen_schedules, fields=('schedule_id', 'schedule_title',
                                                                         'schedule_playlists', 'timeline',
                                                                         'schedule_screens', 'schedule_groups'))
    return obj_to_json_response(json_data)


def get_playlist_schedules(request, playlist_id):
    print "inside get_playlist_schedules"
    playlist_id = int(playlist_id)
    user_details = get_userdetails(request)
    playlist_schedule_id_list = SchedulePlaylists.objects.filter(playlist_id=playlist_id).values_list(
        'schedule_id', flat=True).distinct()
    playlist_schedules = Schedule.get_user_relevant_objects(user_details=user_details).filter(
        schedule_id__in=playlist_schedule_id_list)
    json_data = ScheduleSerializer().serialize(playlist_schedules, fields=('schedule_id', 'schedule_title',
                                                                           'schedule_playlists', 'timeline',
                                                                           'schedule_screens', 'schedule_groups'))
    return obj_to_json_response(json_data)


def get_schedules(request):
    print "inside get_schedules"
    user_details = get_userdetails(request)
    user_schedules = Schedule.get_user_relevant_objects(user_details)

    json_data = ScheduleSerializer().serialize(
        user_schedules, fields=('schedule_id', 'schedule_title', 'schedule_playlists', 'schedule_screens',
                                'schedule_groups', 'timeline'))
    return obj_to_json_response(json_data)


# def get_screen_calendar(request, screen_id):
#     user_details = get_userdetails(request)
#     context_dic = {}
#     try:
#         screen = Screen.get_user_relevant_objects(user_details=user_details).get(screen_id=screen_id)
#         screen_calendar = screen.screen_calendar
#         calendar_slug = screen_calendar.slug
#         context_dic['calendar'] = screen_calendar
#     except Exception as e:
#         print "Exception is ", e
#         return render(request, 'schedule/calendar.html')
#     return calendar(request, calendar_slug=calendar_slug)


@transaction.atomic
@login_required
def delete_schedule(request):
    print "inside delete schedule"
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
        print "Exception is ", e
        success = False
        errors = ['Sorry, you do not have access to this schedule']
    return ajax_response(success=success, errors=errors)
