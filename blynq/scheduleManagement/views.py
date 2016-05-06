import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from schedule.models import Event


# Create your views here.
from customLibrary.serializers import FlatJsonSerializer, playlist_dict
from customLibrary.views_lib import user_and_organization, get_local_time, ajax_response, list_to_json
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
    user_details, organization = user_and_organization(request)
    screen_id = int(screen_id)
    errors = []
    screen_data_json = []
    success = False
    try:
        screen = Screen.get_user_relevant_objects(user_details).get(screen_id=screen_id)
        calendar = screen.screen_calendar
        if calendar:
            current_time = timezone.now()
            calendar_events = calendar.events.exclude(end__lt=current_time)
            start_time = current_time
            end_time = start_time + datetime.timedelta(days=nof_days)
            screen_schedules = ScreenSchedule.objects.filter(event__in=calendar_events)
            for event in calendar_events:
                screen_schedule = screen_schedules.get(event=event)
                schedule = screen_schedule.schedule
                playlist = schedule.playlist
                assert screen_schedule.screen_id == screen_id
                playlist_json = playlist_dict(playlist, only_files=True)
                campaign_dict = {'schedule_id': screen_schedule.schedule.schedule_id,
                                 'playlist': playlist_json,
                                 }
                occurrences = event.get_occurrences(start_time, end_time)
                # campaign_dict = {'schedule' : schedule_json}
                for each_occur in occurrences:
                    campaign_dict['start_time'] = each_occur.start
                    campaign_dict['end_time'] = each_occur.end
                    screen_data_json.append(campaign_dict)
            # print screen_data_json
        success=True
        return list_to_json(screen_data_json)
    except:
        error = "Error while fetching the occurences"
        errors.append(error)
        print error
    return ajax_response(success=success, errors=errors)