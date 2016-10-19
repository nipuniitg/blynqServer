import datetime
import os

from django.db import connection, reset_queries
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from blynq.settings import MEDIA_HOST, HOST_URL
from contentManagement.models import Content
from contentManagement.serializers import default_content_serializer
from customLibrary.custom_settings import PLAYER_POLL_TIME
from customLibrary.views_lib import debugFileLog, string_to_dict, default_string_to_datetime, obj_to_json_response, \
    ajax_response, date_changed, timeit
from playerManagement.helpers import screen_schedule_data
from playerManagement.models import PlayerUpdate, LocalServer, PlayerLog
from playlistManagement.models import PlaylistItems
from reports.models import MediaAnalytics, ScreenAnalytics
from scheduleManagement.models import ScheduleScreens, SchedulePlaylists, SchedulePane
from screenManagement.models import ScreenActivationKey, Screen, FcmDevice
from screenManagement.serializers import default_screen_serializer


# Create your views here.


@csrf_exempt
def player_config(request):
    # posted_data = string_to_dict(request.body)
    # unique_device_key = posted_data.get('device_key')
    config_json = {'host_url': HOST_URL, 'poll_interval': PLAYER_POLL_TIME}
    return obj_to_json_response(config_json)


@csrf_exempt
def player_update_available(request):
    posted_data = string_to_dict(request.body)
    unique_device_key = posted_data.get('device_key')
    version_name = posted_data.get('version_name')
    player_json = {'is_update_available': False, 'url': None}
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
        debugFileLog.exception('Screen activation key %s does not exist' % unique_device_key)
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
    debugFileLog.info("Inside activation_key_valid")
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


def log_query_times(top_results=10):
    queries = connection.queries
    debugFileLog.info('Inside log_query_times, total queries %d' % len(queries))
    newlist = sorted(queries, key=lambda k: float(k['time']))
    newlist.reverse()
    for i in range(top_results):
        debugFileLog.info('Time ' + newlist[i]['time'] + ' Query: ' + newlist[i]['sql'])


@timeit
@csrf_exempt
def get_screen_data(request, nof_days=3):
    """
    :param request: request object should contain device_key ( unique identifier for the screen ) and
                    last_received ( datetime when the screen last polled to the server )
    :param nof_days: optional argument mentioning the time interval for the events
    :return:
    """
    # Uncomment the below line in DEBUG = True and while using log_query_times
    # reset_queries()
    try:
        posted_data = string_to_dict(request.body)
        # the datetime format of last_received should be "%2d%2m%4Y%2H%2M%2S"
        last_received = posted_data.get('last_received')
        unique_device_key = posted_data.get('device_key')
        debugFileLog.info("get_screen_data device_key is %s last_received is %s " % (unique_device_key, last_received))
        last_received_datetime = default_string_to_datetime(last_received)
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(days=nof_days)
        screen = Screen.objects.select_related('screen_data_modified').get(
            unique_device_key__activation_key=unique_device_key)
        is_modified = True
        # Update the screen status saying that it is active
        screen.update_status()
        if date_changed(last_received_datetime):
            is_modified = True
        else:
            is_modified = screen.is_data_modified(last_received_datetime=last_received_datetime)
        campaigns_json = {'campaigns': [], 'is_modified': is_modified}
        if is_modified:
            schedule_ids_list = ScheduleScreens.objects.filter(screen=screen).values_list('schedule_id', flat=True)
            if schedule_ids_list:
                schedule_panes = SchedulePane.objects.select_related(
                    'schedule', 'layout_pane', 'event').prefetch_related('playlists').filter(
                    schedule_id__in=schedule_ids_list).order_by('-schedule__last_updated_time')
                if schedule_panes.exists():
                    screen_data_json = screen_schedule_data(schedule_panes, start_time, end_time)
                    campaigns_json = {'campaigns': screen_data_json, 'is_modified': True}
                # log_query_times()
    except Exception as e:
        errors = "Error while fetching the occurences or invalid screen identifier"
        debugFileLog.exception(errors)
        debugFileLog.exception(e)
        campaigns_json = {'campaigns': [], 'is_modified': False}
    return obj_to_json_response(campaigns_json)


@csrf_exempt
def fcm_register(request):
    try:
        posted_data = string_to_dict(request.body)
        reg_id = posted_data.get('reg_id')  # registration token
        dev_id = posted_data.get('dev_id')
        fcm_device, created = FcmDevice.objects.update_or_create(dev_id=dev_id,
                                                                 defaults={'reg_id': reg_id, 'is_active': True})
        try:
            screen = Screen.objects.get(unique_device_key__activation_key=dev_id)
        except Exception as e:
            debugFileLog.exception('Error while extracting screen object from device id')
            debugFileLog.exception(e)
            return ajax_response(success=False)
        screen.fcm_device = fcm_device
        screen.save()
        success = True
    except Exception as e:
        debugFileLog.exception('Error while saving the fcm device to database')
        debugFileLog.exception(e)
        success = False
    return ajax_response(success=success)


@csrf_exempt
def media_stats(request):
    debugFileLog.info('Inside media stats player')
    try:
        posted_data = string_to_dict(request.body)
        unique_device_key = posted_data.get('device_key')
        screen = Screen.objects.get(unique_device_key__activation_key=unique_device_key)
        media_stats_list = posted_data.get('media_item_stats_list')
        for stat in media_stats_list:
            try:
                content_id = int(stat.get('content_id'))
                playlist_id = int(stat.get('playlist_id'))
                count = int(stat.get('count'))
                time_played = stat.get('time_played')
                time_played = int(time_played) if time_played else 0
                date = stat.get('date')
                converted_date = default_string_to_datetime(date, fmt='%Y-%m-%d')
                media_analytics = MediaAnalytics(screen=screen, content_id=content_id, playlist_id=playlist_id,
                                                 count=count, date=converted_date, time_played=time_played)
                media_analytics.save()
            except Exception as e:
                debugFileLog.exception('Improper media analytics data')
                debugFileLog.exception(e)
        screen_stats = posted_data.get('session_time_list')
        for stat in screen_stats:
            try:
                start_time = stat.get('session_start_time')
                session_start_time = default_string_to_datetime(start_time)
                end_time = stat.get('session_end_time')
                session_end_time = default_string_to_datetime(end_time)
                screen_analytics = ScreenAnalytics(screen=screen, session_start_time=session_start_time,
                                                   session_end_time=session_end_time)
                screen_analytics.save()
            except Exception as e:
                debugFileLog.exception(e)
        success = True
    except Exception as e:
        success = False
        debugFileLog.exception(e)
    return ajax_response(success=success)


@csrf_exempt
def insert_logs(request):
    debugFileLog.info('Inside insert player logs')
    try:
        for key in request.FILES.keys():
            file = request.FILES[key]
            player_log = PlayerLog(file=file)
            player_log.save()
        success = True
    except Exception as e:
        debugFileLog.exception(e)
        success = False
    return ajax_response(success=success)


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
        json_data = default_content_serializer(contents, fields=('document'))
        url_list = [str(element['url']) for element in json_data]
        json_obj = dict()
        json_obj['urls'] = url_list
        json_obj['success'] = True
        return obj_to_json_response(json_obj)
    except Exception as e:
        debugFileLog.exception(e)
        success = False
        errors = str(e)
        return ajax_response(success=success, errors=errors)


@csrf_exempt
def update_status(request):
    try:
        posted_data = string_to_dict(request.body)
        unique_device_key = posted_data.get('device_key')
        if not unique_device_key:
            raise Exception('Device key is empty')
        screen = Screen.objects.get(unique_device_key__activation_key=unique_device_key)
        screen.update_status()
        success = True
    except Exception as e:
        debugFileLog.exception(e)
        success = False
    return ajax_response(success=success)


@csrf_exempt
def screen_info(request):
    debugFileLog.info('Inside screen info')
    unique_device_key = ''
    try:
        posted_data = string_to_dict(request.body)
        unique_device_key = posted_data.get('device_key')
        screen = Screen.objects.filter(unique_device_key__activation_key=unique_device_key)
        json_data = default_screen_serializer(screen, fields=('screen_name', 'address', 'screen_size',
                                                              'aspect_ratio', 'resolution', 'last_active_time'))
        if json_data and type(json_data) == list:
            return obj_to_json_response(json_data[0])
    except Exception as e:
        debugFileLog.exception('Exception while fetching screen info for device key %s' % unique_device_key)
        debugFileLog.exception(e)
    return obj_to_json_response({})
