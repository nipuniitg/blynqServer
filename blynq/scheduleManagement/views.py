import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedule.models import Event


# Create your views here.
from customLibrary.serializers import FlatJsonSerializer, playlist_dict
from customLibrary.views_lib import user_and_organization, get_local_time, ajax_response, list_to_json, string_to_dict
from scheduleManagement.models import Schedule, ScreenSchedule
from screenManagement.models import Screen


@login_required
def index(request):
    return render(request,'scheduleManagement/schedule_index.html')


@login_required
def upsert_schedule(request, schedule_id = -1):
    #if(schedule_id == -1):
    return render(request, 'scheduleManagement/schedule_details.html')


def get_screen_data(request, screen_id, nof_days=7):
    # TODO: Login system for screens
    # user_details, organization = user_and_organization(request)
    screen_id = int(screen_id)
    errors = []
    screen_data_json = []
    success = False
    try:
        screen = Screen.objects.get(screen_id=screen_id)
        calendar = screen.screen_calendar
        if calendar:
            current_time = timezone.now()
            calendar_events = calendar.events.exclude(end_recurring_period__lt=current_time)
            start_time = current_time
            end_time = start_time + datetime.timedelta(days=nof_days)
            screen_schedules = ScreenSchedule.objects.filter(event__in=calendar_events)
            for event in calendar_events:
                screen_schedule = screen_schedules.get(event=event)
                schedule = screen_schedule.schedule
                assert screen_schedule.screen_id == screen_id
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
                occurrences = event.get_occurrences(start_time, end_time)
                for each_occur in occurrences:
                    campaign_dict['start_time'] = each_occur.start
                    campaign_dict['end_time'] = each_occur.end
                    screen_data_json.append(campaign_dict)
            # print screen_data_json
        campaigns_json = {'campaigns': screen_data_json}
        success = True
        return list_to_json(campaigns_json)
    except:
        error = "Error while fetching the occurences"
        errors.append(error)
        print error
    return ajax_response(success=success, errors=errors)


def get_schedules(request):
    user_details, organization = user_and_organization(request)
    user_schedules = Schedule.get_user_relevant_objects(user_details)
    json_data = FlatJsonSerializer().serialize(user_schedules,
                                               fields=('schedule_id', 'schedule_title', 'playlist', 'screens',))


def run_playlist(request):
    user_details, organization = user_and_organization(request)


# def upsert_schedule(request):
#     errors = []
#     success = False
#     user_details, organization = user_and_organization(request)
#     try:
#         # Extract data from request.body
#         posted_data = string_to_dict(request.body)
#         schedule_id = int(posted_data.get('schedule_id'))
#         schedule_title = posted_data.get('schedule_title')
#     except:
#         error = 'Error while upserting schedule'
#         print error
#         errors.append(error)

