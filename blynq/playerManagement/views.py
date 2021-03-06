import datetime

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from blynq.settings import HOST_URL
from contentManagement.models import Content
from contentManagement.serializers import default_content_serializer
from customLibrary.custom_settings import PLAYER_POLL_TIME, PLAYER_NOTIFY_MAIL
from customLibrary.views_lib import debugFileLog, string_to_dict, default_string_to_datetime, obj_to_json_response, \
    ajax_response, date_changed, timeit, mail_exception, empty_list_for_none, send_mail_blynq, empty_string_for_none
from playerManagement.helpers import screen_schedule_data
from playerManagement.models import PlayerUpdate, LocalServer, PlayerLog
from playlistManagement.models import PlaylistItems
from reports.models import MediaAnalytics, ScreenAnalytics
from scheduleManagement.models import ScheduleScreens, SchedulePlaylists, SchedulePane
from screenManagement.models import ScreenActivationKey, Screen, FcmDevice


# Create your views here.


@csrf_exempt
def player_config(request):
    # posted_data = string_to_dict(request.body)
    # unique_device_key = posted_data.get('device_key')
    config_json = {'host_url': HOST_URL, 'poll_interval': PLAYER_POLL_TIME}
    return obj_to_json_response(config_json)


@csrf_exempt
def player_update_available(request):
    player_json = {'is_update_available': False, 'url': None}
    try:
        posted_data = string_to_dict(request.body)
        unique_device_key = posted_data.get('device_key')
        version = int(posted_data.get('version'))
        screen_activation_key = ScreenActivationKey.objects.get(activation_key=unique_device_key)
        screen = screen_activation_key.screen
        if screen.update_app:
            updates = PlayerUpdate.objects.all()
            if updates.exists():
                last_update = updates[0]
                if last_update.version > version:
                    player_json['is_update_available'] = True
                    player_json['url'] = last_update.apk_url
    except ScreenActivationKey.DoesNotExist:
        debugFileLog.exception('Screen activation key does not exist for request body' % request.body)
    except Exception as e:
        mail_exception(exception=e)
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
        if screen_activation_key.in_use:
            success = True
        else:
            success = False
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


@timeit
@csrf_exempt
def get_screen_data(request, nof_days=3):
    """
    :param request: request object should contain device_key ( unique identifier for the screen ) and
                    last_received ( datetime when the screen last polled to the server )
    :param nof_days: optional argument mentioning the time interval for the events
    :return:
    """
    campaigns_json = {'campaigns': [], 'is_modified': False}
    try:
        posted_data = string_to_dict(request.body)
        # the datetime format of last_received should be "%2d%2m%4Y%2H%2M%2S"
        last_received = posted_data.get('last_received')
        unique_device_key = posted_data.get('device_key')
        debugFileLog.info("get_screen_data device_key is %s last_received is %s " % (unique_device_key, last_received))
        last_received_datetime = default_string_to_datetime(last_received)
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(days=nof_days)
        try:
            screen = Screen.objects.select_related('screen_data_modified').get(
                unique_device_key__activation_key=unique_device_key)
        except Exception as e:
            debugFileLog.error(e)
            return obj_to_json_response(campaigns_json)
        # Update the screen status saying that it is active
        # TODO: update_status might not required as there is already api/player/ping
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
                    schedule_id__in=schedule_ids_list).order_by('-schedule__last_updated_time', 'layout_pane__z_index')
                if schedule_panes.exists():
                    screen_data_json = screen_schedule_data(schedule_panes, start_time, end_time)
                    campaigns_json = {'campaigns': screen_data_json, 'is_modified': True}
    except Exception as e:
        errors = "Error while fetching the occurrences or invalid screen identifier"
        debugFileLog.exception(errors)
        mail_exception(exception=e)
    return obj_to_json_response(campaigns_json)


@csrf_exempt
def fcm_register(request):
    posted_data = string_to_dict(request.body)
    reg_id = posted_data.get('reg_id')  # registration token
    dev_id = posted_data.get('dev_id')
    success = FcmDevice.update_token(device_key=dev_id, reg_id=reg_id)
    return ajax_response(success=success)


@csrf_exempt
def media_stats(request):
    """
    :param request:
    :param request.body {'device_key': 1234567890, 'version_id': 4.12, 'reg_id': 'abcdefghijk',
    'media_item_stats_list': [], 'session_time_list': []}
    :return: success, fcm_success
    """
    debugFileLog.info('Inside media stats player')
    fcm_success = False
    try:
        posted_data = string_to_dict(request.body)
        unique_device_key = posted_data.get('device_key')
        screen = Screen.objects.get(unique_device_key__activation_key=unique_device_key)
        debugFileLog.info(' for screen %s with key %s' % (screen.screen_name, unique_device_key))
        version_id = posted_data.get('version_id')
        debugFileLog.info('device_key %s has app version %s' % (str(unique_device_key), str(version_id)))
        if version_id:
            screen.app_version = int(version_id)
            screen.save()
        reg_id = posted_data.get('reg_id')
        if reg_id:
            fcm_success = FcmDevice.update_token(device_key=unique_device_key, reg_id=reg_id)
        # Only save the reports for Selected clients
        if not screen.owned_by.enable_reports:
            return ajax_response(success=True, obj_dict={'fcm_success': fcm_success})
        media_stats_list = empty_list_for_none(posted_data.get('media_item_stats_list'))
        for stat in media_stats_list:
            try:
                content_id = int(stat.get('content_id'))
                playlist_id = int(stat.get('playlist_id'))
                count = int(stat.get('count'))
                time_played = stat.get('time_played')
                time_played = int(time_played) if time_played else 0
                date = stat.get('date')
                if not date:
                    continue
                converted_date = default_string_to_datetime(date, fmt='%Y-%m-%d')
                media_analytics = MediaAnalytics(screen=screen, content_id=content_id, playlist_id=playlist_id,
                                                 count=count, date=converted_date, time_played=time_played)
                media_analytics.save()
            except Exception as e:
                debugFileLog.exception('Improper media analytics data')
                debugFileLog.error(e)
                # mail_exception(exception=e)
        screen_stats = empty_list_for_none(posted_data.get('session_time_list'))
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
                debugFileLog.error(e)
                # mail_exception(exception=e)
        success = True
    except Exception as e:
        success = False
        fcm_success = False
        # mail_exception(exception=e)
    return ajax_response(success=success, obj_dict={'fcm_success': fcm_success})


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
        mail_exception(exception=e)
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
        mail_exception(exception=e)
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
        mail_exception(exception=e)
        success = False
    return ajax_response(success=success)


@csrf_exempt
def screen_info(request):
    debugFileLog.info('Inside screen info')
    device_key = ''
    try:
        posted_data = string_to_dict(request.body)
        device_key = posted_data.get('device_key')
        screen_json = Screen.get_info(device_key=device_key)
        return obj_to_json_response(screen_json)
    except Exception as e:
        debugFileLog.exception('Exception while fetching screen info for device key %s' % unique_device_key)
        mail_exception(exception=e)
    return obj_to_json_response({})


@csrf_exempt
def send_mail(request):
    try:
        posted_data = string_to_dict(request.body)
        device_key = posted_data.get('device_key')
        screen_json = Screen.get_info(device_key=device_key)
        subject = empty_string_for_none(posted_data.get('subject'))
        message = empty_string_for_none(posted_data.get('message'))
        full_message = str(screen_json) + '  \n   ' + message
        send_mail_blynq(to=PLAYER_NOTIFY_MAIL, subject=subject, message=full_message)
        success = True
    except Exception as e:
        debugFileLog.error("Sending mail for player log failed")
        debugFileLog.error(e)
        success = False
    return ajax_response(success=success)
