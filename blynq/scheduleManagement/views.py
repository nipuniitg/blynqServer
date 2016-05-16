import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedule.models import Event, Rule


# Create your views here.
from customLibrary.serializers import playlist_dict, schedule_dict
from customLibrary.views_lib import get_userdetails, ajax_response, list_to_json, string_to_dict, list_to_comma_string, \
    default_string_to_datetime
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
    params = interval_param(interval)
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekday', bylistday=byweekday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='bymonthday', bylistday=bymonthday))
    params = append_params(params=params, new_keyvalue=list_to_param(key_str='byweekno', bylistday=byweekno))
    return params


def upsert_schedule_screens(user_details, schedule, schedule_screens, event_dict):
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
                Event.objects.filter(id=entry.event.id).update(**event_dict)
                entry.save()
            schedule_screen_id_list.append(schedule_screen_id)

        # Remove screens not in the schedule
        removed_schedule_screens = ScheduleScreens.objects.filter(schedule=schedule, group__isnull=True).exclude(
            schedule_screen_id__in=schedule_screen_id_list)
        for schedule_screen in removed_schedule_screens:
            schedule_screen.delete()
        success = True
        return success, error
    except:
        error = 'Error while upserting screens in schedule'
        print error
        return success, error


def upsert_schedule_groups(user_details, schedule, schedule_groups, event_dict):
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
    except:
        error = 'Error while upserting groups in schedule'
        print error
        return success, error


# upsert schedule playlists
def upsert_schedule_playlists(user_details, schedule, schedule_playlists):
    success = False
    error = ''
    try:
        schedule_playlist_id_list = []
        for pos_index, item in enumerate(schedule_playlists):
            schedule_playlist_id = int(item.get('schedule_playlist_id'))
            playlist_str = item.get('playlist')
            playlist_id = int(playlist_str.get('playlist_id'))
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
    except:
        error = 'Error while upserting playlists in schedule'
        print error
        return success, error


def generate_rule(timeline, name, description):
    interval = int(timeline.get('interval'))
    byweekno = timeline.get('byweekno')
    bymonthday = timeline.get('bymonthday')
    byweekday = timeline.get('byweekday')
    params = generate_rule_params(interval=interval, bymonthday=bymonthday, byweekday=byweekday, byweekno=byweekno)
    rule = Rule(name=name, description=description, params=params)
    rule.save()
    return rule


def event_for_allday(schedule, timeline):
    start_date = timeline.get('start_date')
    start_time = datetime.time(0)
    start = datetime.datetime.combine(start_date, start_time)
    end_date = start_date
    end_time = datetime.time(23, 59, 59, 999)
    end = datetime.datetime.combine(end_date, end_time)
    end_recurring_period_date = timeline.get('end_recurring_period')
    end_recurring_period = datetime.datetime.combine(end_recurring_period_date, end_time)
    rule = generate_rule(timeline=timeline, name=schedule.schedule_title, description=schedule.schedule_title)
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': schedule.created_by,
                  'rule': rule}
    return event_dict


def event_for_always(schedule):
    start_date = datetime.datetime.today()
    start_time = datetime.time(0)
    start = datetime.datetime.combine(start_date, start_time)
    end_date = start_date
    end_time = datetime.time(23, 59, 59, 999)
    end = datetime.datetime.combine(end_date, end_time)
    rule = default_rule(frequency='DAILY')
    event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': schedule.created_by,
                  'rule': rule}
    return event_dict


def event_dict_from_timeline(timeline, schedule):
    is_always = timeline.get('is_always')
    all_day = timeline.get('all_day')
    if is_always:
        return event_for_always(schedule)
    elif all_day:
        return event_for_allday(schedule, timeline)
    else:
        start_date = timeline.get('start_date')
        start_time = timeline.get('start_time')
        start = datetime.datetime.combine(start_date, start_time)
        end_date = start_date
        end_time = timeline.get('end_time')
        end = datetime.datetime.combine(end_date, end_time)
        end_recurring_period_time = end_time
        end_recurring_period = timeline.get('end_recurring_period')
        end_recurring_period = datetime.datetime.combine(end_recurring_period, end_recurring_period_time)
        rule = generate_rule(timeline, name=schedule.schedule_title, description=schedule.schedule_title)
        event_dict = {'start': start, 'end': end, 'title': schedule.schedule_title, 'creator': schedule.created_by,
                      'rule': rule, 'end_recurring_period': end_recurring_period}
        return event_dict


@login_required
def upsert_schedule(request):
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
        user_schedules = Schedule.get_user_relevant_objects(user_details=user_details)

        # upsert schedule
        if schedule_id == -1:
            schedule = Schedule.objects.create(schedule_title=schedule_title, created_by=user_details,
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
    except:
        error = 'Error while upserting content to schedule'
        print error
        errors.append(error)
    return ajax_response(success=success, errors=errors)


def get_screen_data(request, screen_id, last_received, nof_days=7):
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
            screen_schedules = ScheduleScreens.objects.filter(event__in=calendar_events)
            if not calendar_events:
                is_modified = True
            for event in calendar_events:
                try:
                    screen_schedule = screen_schedules.get(event=event)
                except:
                    print 'Event does not exist in the schedule screens'
                    continue
                schedule = screen_schedule.schedule
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
                campaign_dict = {'schedule_id': screen_schedule.schedule.schedule_id,
                                 'playlists': playlists_json,
                                 'last_updated_time': schedule.last_updated_time,
                                 }
                for each_occur in occurrences:
                    campaign_dict['start_time'] = each_occur.start
                    campaign_dict['end_time'] = each_occur.end
                    screen_data_json.append(campaign_dict)
            # print screen_data_json
        campaigns_json = {'campaigns': screen_data_json, 'is_modified': is_modified}
        success = True
        return list_to_json(campaigns_json)
    except:
        error = "Error while fetching the occurences or invalid screen identifier"
        errors.append(error)
        print error
    return ajax_response(success=success, errors=errors)


def get_schedules(request):
    user_details = get_userdetails(request)
    user_schedules = Schedule.get_user_relevant_objects(user_details)
    all_schedules = []
    for schedule in user_schedules:
        schedule_dictionary = schedule_dict(schedule)
        all_schedules.append(schedule_dictionary)
    return list_to_json(all_schedules)


@login_required
def get_schedule_details(request,schedule_id):
    user_details = get_userdetails(request)
    context_dic = {}
    if schedule_id == -1:
        context_dic['schedule'] = {}
        context_dic['relevant'] = True
    else:
        try:
            schedule = Schedule.get_user_relevant_objects(user_details=user_details).get(schedule_id=schedule_id)
            schedule_dictionary = schedule_dict(schedule)
            context_dic['relevant'] = True
            context_dic['schedule'] = schedule_dictionary
        except:
            context_dic['relevant'] = False
    #return JsonResponse(context_dic)
    return render(request,'scheduleManagement/schedule_details.html',context_dic)