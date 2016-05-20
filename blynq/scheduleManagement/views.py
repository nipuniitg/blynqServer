import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedule.models import Event, Rule


# Create your views here.
from customLibrary.serializers import playlist_dict, schedule_dict
from customLibrary.views_lib import get_userdetails, ajax_response, list_to_json, string_to_dict, list_to_comma_string, \
    default_string_to_datetime, get_utc_datetime
from playlistManagement.models import Playlist
from scheduleManagement.models import Schedule, ScheduleScreens, SchedulePlaylists
from screenManagement.models import Screen, Group


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
    success = False
    error = ''
    try:
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
        for each_schedule_screen in removed_schedule_screens:
            if each_schedule_screen.event:
                if each_schedule_screen.event.rule:
                    each_schedule_screen.event.rule.delete()
                each_schedule_screen.event.delete()
        if removed_schedule_screens:
            removed_schedule_screens.delete()
        success = True
        return success, error
    except Exception as e:
        print "Exception is ", e
        error = 'Error while upserting screens in schedule'
        print error
        return success, error


def upsert_schedule_groups(user_details, schedule, schedule_groups, event_dict):
    print "inside upsert_schedule_groups"
    success = False
    error = ''
    try:
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
                entry = ScheduleScreens.objects.create(schedule=schedule, group=group, event=event)
                for screen in group.screen_set.all():
                    screen_event = Event(**event_dict)
                    screen_event.calendar = screen.screen_calendar
                    screen_event.save()
                    entry = ScheduleScreens.objects.create(screen=screen, schedule=schedule, group=group,
                                                           event=screen_event)
                schedule_screen_id = entry.schedule_screen_id
            else:
                entry = ScheduleScreens.objects.get(schedule_screen_id=schedule_screen_id)
                Event.objects.filter(id=entry.event.id).update(**event_dict)
                entry.save()
            schedule_screen_id_list.append(schedule_screen_id)
            
        # Remove groups not in the schedule
        removed_schedule_groups = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=False).exclude(
            schedule_screen_id__in=schedule_screen_id_list)
        for schedule_group in removed_schedule_groups:
            schedule_group.delete()
        success = True
        return success, error
    except Exception as e:
        print "Exception is ", e
        error = 'Error while upserting groups in schedule'
        print error
        return success, error


# upsert schedule playlists
def upsert_schedule_playlists(user_details, schedule, schedule_playlists):
    print "inside upsert_schedule_playlists"
    success = False
    error = ''
    try:
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
    except Exception as e:
        print "Exception is ", e
        error = 'Error while upserting playlists in schedule'
        print error
        return success, error


def generate_rule(timeline, name, description):
    print "inside generate_rule"
    interval = int(timeline.get('interval'))
    byweekno = timeline.get('byweekno')
    bymonthday = timeline.get('bymonthday')
    byweekday = timeline.get('byweekday')
    frequency = timeline.get('frequency')
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
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': schedule.created_by,
                  'rule': rule, 'end_recurring_period': end_recurring_period}
    return event_dict


def event_for_always(schedule):
    print "inside event_for_always"
    start = timezone.now().replace(hour=0, minute=0, second=0)
    end = timezone.now().replace(hour=23, minute=59, second=59)
    rule = Rule(name=schedule.schedule_title, description=schedule.schedule_title, frequency='DAILY')
    rule.save()
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': schedule.created_by,
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
        event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': schedule.created_by,
                      'rule': rule, 'end_recurring_period': end_recurring_period}
        return event_dict


@login_required
def upsert_schedule(request):
    print "inside upsert_schedule"
    errors = []
    success = False
    user_details = get_userdetails(request)
    try:
        # Extract data from request.body
        posted_data = string_to_dict(request.body)
        schedule_id = int(posted_data.get('schedule_id'))
        schedule_title = posted_data.get('schedule_title')
        schedule_playlists = posted_data.get('schedule_playlists')
        schedule_screens = posted_data.get('schedule_screens')
        schedule_groups = posted_data.get('schedule_groups')
        timeline = posted_data.get('timeline')
        print 'timeline is'
        print timeline
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
        print "Exception is ", e
        error = 'Error while upserting content to schedule'
        errors.append(error)
        print errors
    return ajax_response(success=success, errors=errors)


def get_screen_data(request, screen_id, last_received, nof_days=7):
    print "inside get_screen_data"
    # TODO: Login system for screens
    # user_details, organization = user_and_organization(request)
    screen_id = int(screen_id)
    errors = []
    screen_data_json = []
    success = False
    is_modified = False
    last_received_datetime = default_string_to_datetime(last_received)
    try:
        screen = Screen.objects.get(screen_id=screen_id)
        calendar = screen.screen_calendar
        if calendar:
            current_time = timezone.now()
            calendar_events = calendar.events.exclude(end_recurring_period__lt=current_time)
            start_time = current_time
            end_time = start_time + datetime.timedelta(days=nof_days)
            completed_schedules = []
            if not calendar_events:
                is_modified = True
            for event in calendar_events:
                try:
                    # Each event should have only one entry in Schedule_Screens
                    screen_schedule = event.schedulescreens.all()[0]
                except Exception as e:
                    print "Exception is ", e
                    print 'Event does not exist in the schedule screens'
                    continue
                schedule = screen_schedule.schedule
                if schedule.schedule_id in completed_schedules:
                    continue
                else:
                    completed_schedules.append(schedule.schedule_id)
                if schedule.last_updated_time < last_received_datetime:
                    continue
                else:
                    is_modified = True
                # assert screen_schedule.screen_id == screen_id
                occurrences = event.get_occurrences(start_time, end_time)
                if not occurrences:
                    is_modified = True
                    continue
                # TODO: optimize this
                playlists = schedule.playlists.all()
                playlists_json = []
                for playlist in playlists:
                    playlist_json = playlist_dict(playlist, only_files=True)
                    playlists_json.append(playlist_json)
                for each_occur in occurrences:
                    campaign_dict = {'schedule_id': screen_schedule.schedule.schedule_id, 'playlists': playlists_json,
                                     'last_updated_time': schedule.last_updated_time, 'start_time': each_occur.start,
                                     'end_time': each_occur.end}
                    screen_data_json.append(campaign_dict)
        else:
            is_modified = True
        campaigns_json = {'campaigns': screen_data_json, 'is_modified': is_modified}
        success = True
        return list_to_json(campaigns_json)
    except Exception as e:
        print "Exception is ", e
        error = "Error while fetching the occurences or invalid screen identifier"
        errors.append(error)
        print error
    return ajax_response(success=success, errors=errors)


def get_screen_schedules(request, screen_id):
    print "inside get_screen_schedules"
    screen_id = int(screen_id)
    user_details = get_userdetails(request)
    screen_schedule_id_list = ScheduleScreens.objects.filter(screen_id=screen_id).values_list(
        'schedule_id', flat=True).distinct()
    screen_schedules = Schedule.get_user_relevant_objects(user_details).filter(schedule_id__in=screen_schedule_id_list)
    relevant_schedules = []
    for schedule in screen_schedules:
        schedule_dictionary = schedule_dict(schedule)
        relevant_schedules.append(schedule_dictionary)
    return list_to_json(relevant_schedules)


def get_playlist_schedules(request, playlist_id):
    print "inside get_playlist_schedules"
    playlist_id = int(playlist_id)
    user_details = get_userdetails(request)
    playlist_schedule_id_list = SchedulePlaylists.objects.filter(playlist_id=playlist_id).values_list(
        'schedule_id', flat=True).distinct()
    playlist_schedules = Schedule.get_user_relevant_objects(user_details=user_details).filter(
        schedule_id__in=playlist_schedule_id_list)
    relevant_schedules = []
    for schedule in playlist_schedules:
        schedule_dictionary = schedule_dict(schedule)
        relevant_schedules.append(schedule_dictionary)
    return list_to_json(relevant_schedules)


def get_schedules(request):
    print "inside get_schedules"
    user_details = get_userdetails(request)
    user_schedules = Schedule.get_user_relevant_objects(user_details)
    all_schedules = []
    for schedule in user_schedules:
        schedule_dictionary = schedule_dict(schedule)
        all_schedules.append(schedule_dictionary)
    return list_to_json(all_schedules)


@login_required
def delete_schedule(request):
    print "inside delete schedule"
    user_details = get_userdetails(request)
    errors = []
    success = False
    try:
        posted_data = string_to_dict(request.body)
        print 'body is ',request.body
        schedule_id = int(posted_data.get('schedule_id'))
        schedule = Schedule.get_user_relevant_objects(user_details=user_details).get(schedule_id=schedule_id)
        schedule.delete()
        success = True
    except Exception as e:
        print "Exception is ", e
        success = False
        errors = ['Sorry, you do not have access to this schedule']
    return ajax_response(success=success, errors=errors)
