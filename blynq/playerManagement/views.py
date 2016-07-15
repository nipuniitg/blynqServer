import datetime
import os

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from blynq.settings import MEDIA_HOST
from contentManagement.models import Content
from contentManagement.serializers import ContentSerializer
from customLibrary.views_lib import debugFileLog, string_to_dict, default_string_to_datetime, obj_to_json_response, \
    ajax_response
from playerManagement.models import PlayerUpdate
from playlistManagement.models import PlaylistItems
from playlistManagement.serializers import PlaylistSerializer
from scheduleManagement.models import ScheduleScreens, SchedulePlaylists
from screenManagement.models import ScreenActivationKey, Screen


@csrf_exempt
def player_update_available(request):
    errors = []
    posted_data = string_to_dict(request.body)
    unique_device_key = posted_data.get('device_key')
    version_name = posted_data.get('version_name')
    player_json={'is_update_available': False, 'url': None}
    try:
        screen = ScreenActivationKey.objects.get(activation_key=unique_device_key, verified=True)
        updates = PlayerUpdate.objects.order_by('-uploaded_time')
        if updates:
            full_filename = os.path.basename(updates[0].executable.name)
            filename = os.path.splitext(full_filename)[0]
            if filename != version_name:
                player_json['is_update_available'] = True
                player_json['url'] = MEDIA_HOST + updates[0].executable.url
    except ScreenActivationKey.DoesNotExist:
        debugFileLog.exception('Screen activation key does not exist')
    except Exception as e:
        debugFileLog.exception(e)
    return obj_to_json_response(player_json)


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
        elif screen_activation_key.in_use:
            success = True
        else:
            success = False
    except ScreenActivationKey.DoesNotExist:
        error = 'Activation key %s doesn\'t exist in the database.\n ' % activation_key
        error += 'Adding it, check the verified boolean if the device is valid.\n'
        debugFileLog.warning(error)
        try:
            screen_activation_key = ScreenActivationKey(activation_key=activation_key, verified=True)
            screen_activation_key.save()
        except Exception as e:
            db_error = 'Adding the above activation_key to the database failed with the exception {0} \n'.format(str(e))
            debugFileLog.error(db_error)
        success = False
    return ajax_response(success=success, errors=error)


@csrf_exempt
def activation_key_valid(request):
    debugFileLog.info( "Inside activation_key_valid" )
    return device_key_active(request)
    # posted_data = string_to_dict(request.body)
    # activation_key = posted_data.get('device_key')
    # debugFileLog.exception("%s " % activation_key )
    # errors = []
    # try:
    #     screen_activation_key = ScreenActivationKey.objects.get(activation_key=activation_key, in_use=True, verified=True)
    #     success = True
    # except ScreenActivationKey.DoesNotExist:
    #     errors = ['Invalid activation key, try another or contact support']
    #     success = False
    # except Exception as e:
    #     success = False        
    #     errors = ['Invalid activation key, try another or contact support']
    # return ajax_response(success=success, errors=errors)


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
    debugFileLog.info( "device_key is %s last_received is %s " % ( unique_device_key, last_received ) )
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
