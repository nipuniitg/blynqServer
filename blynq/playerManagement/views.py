import datetime
import os
from copy import deepcopy
from operator import itemgetter
from django.shortcuts import render
# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from blynq.settings import MEDIA_HOST, HOST_URL, PLAYER_POLL_TIME
from contentManagement.models import Content
from contentManagement.serializers import ContentSerializer
from customLibrary.views_lib import debugFileLog, string_to_dict, default_string_to_datetime, obj_to_json_response, \
    ajax_response, date_changed
from playerManagement.models import PlayerUpdate, LocalServer
from playlistManagement.models import PlaylistItems
from playlistManagement.serializers import PlaylistSerializer
from scheduleManagement.models import ScheduleScreens, SchedulePlaylists, SchedulePane
from screenManagement.models import ScreenActivationKey, Screen, ORIENTATION_CHOICES, FcmDevice
from layoutManagement.serializers import default_layout_pane_serializer
from screenManagement.serializers import AspectRatioSerializer


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


def schedule_pane_from_occurrence(occur):
    return occur.event.schedulepane_event


def is_conflicting(cur_occur, new_occur):
    """
    :param cur_occur: this event occurrence has more priority
    :param new_occur: this event occurrence has less priority
    :return: True if both the occurrences have the same schedule_pane and cur_occur overlaps with occur, else False
    """
    try:
        cur_schedule_pane = schedule_pane_from_occurrence(cur_occur)
        new_schedule_pane = schedule_pane_from_occurrence(new_occur)
        if cur_schedule_pane.schedule_id == new_schedule_pane.schedule_id:
            # Two occurrences of the same schedule can never conflict
            return False
        elif cur_schedule_pane.schedule.layout_id == new_schedule_pane.schedule.layout_id and \
                        cur_schedule_pane.layout_pane_id != new_schedule_pane.layout_pane_id:
            # Two occurrences from same layout and different layout_pane_id can never conflict
            return False
        elif (cur_occur.start <= new_occur.start <= cur_occur.end) or (new_occur.start <= cur_occur.start <= new_occur.end):
            return True
    except Exception as e:
        debugFileLog.exception(e)
    return False


def merge_occurrence(existing_occurrences, new_occur):
    """
    :param new_occur: new event occurrence which has low priority compared to event occurrences in existing_occurrences
    :param existing_occurrences: the list of event occurrences computed till now
    :return: modified existing_occurrences based on the start_time and end_time of the new occurrence
    """
    # Merge the new occur into existing_occurrences
    # two occurrences are overlapping only if layout_pane_id is same and time period overlaps
    new_occur_parts = []
    for cur_occur in existing_occurrences:
        if is_conflicting(cur_occur, new_occur):
            # compare start times with < and end times with >
            if new_occur.start < cur_occur.start:
                if new_occur.end <= cur_occur.end:
                    new_occur.end = cur_occur.start
                else:
                    new_occur_part = deepcopy(new_occur)
                    new_occur.end = cur_occur.start
                    new_occur_part.start = cur_occur.end
                    new_occur_parts.append(new_occur_part)
            else:
                if new_occur.end <= cur_occur.end:
                    # new_occur lies in between cur_occur
                    new_occur = None
                    break
                else:
                    new_occur.start = cur_occur.end
    if new_occur:
        existing_occurrences.append(new_occur)
    for each_new_occur_part in new_occur_parts:
        existing_occurrences = merge_occurrence(existing_occurrences, each_new_occur_part)
    return existing_occurrences


def event_json_from_occurrences(existing_occurrences):
    screen_data_json = []
    for occur in existing_occurrences:
        schedule_pane = schedule_pane_from_occurrence(occur)
        schedule = schedule_pane.schedule
        playlists = schedule_pane.playlists.all()
        playlists_json = PlaylistSerializer().serialize(playlists, fields=('playlist_id', 'playlist_title',
                                                                           'playlist_items'))
        aspect_ratio_list = [schedule.layout.aspect_ratio] if schedule.layout and schedule.layout.aspect_ratio else []
        aspect_ratio = AspectRatioSerializer().serialize(aspect_ratio_list)
        orientation = aspect_ratio[0]['orientation'] if aspect_ratio else ORIENTATION_CHOICES[0][0]
        layout_pane_dict = default_layout_pane_serializer([schedule_pane.layout_pane])[0]
        layout_pane_dict['orientation'] = orientation
        campaign_dict = {'schedule_id': schedule.schedule_id,
                         'playlists': playlists_json,
                         'pane': layout_pane_dict,
                         'last_updated_time': schedule.last_updated_time,
                         'start_time': occur.start,
                         'end_time': occur.end}
        screen_data_json.append(campaign_dict)
    sorted_screen_data = sorted(screen_data_json, key=itemgetter('start_time'))
    return sorted_screen_data


def screen_schedule_data(schedule_panes, start_time, end_time):
    """
    :param schedule_panes: schedule_panes should be sorted descending by last_updated_time of the schedule
    :param start_time: start_time of the time interval to calculate event occurrences
    :param end_time: end_time of the time interval to calculate event occurrences
    :return: schedule data of non-overlapping event occurrences
    """
    existing_occurrences = []
    for obj in schedule_panes:
        if obj.event:
            event_occurrences = obj.event.get_occurrences(start_time, end_time)
            # existing_occurrences.update(event_occurrences)
            # Comment below two lines and uncomment above line if merging is to be removed
            for new_occur in event_occurrences:
                existing_occurrences = merge_occurrence(existing_occurrences, new_occur)
    return event_json_from_occurrences(existing_occurrences)


@csrf_exempt
def get_screen_data(request, nof_days=7):
    """
    :param request: request object should contain device_key ( unique identifier for the screen ) and
                    last_received ( datetime when the screen last polled to the server )
    :param nof_days: optional argument mentioning the time interval for the events
    :return:
    """
    posted_data = string_to_dict(request.body)
    # the datetime format of last_received should be "%2d%2m%4Y%2H%2M%2S"
    last_received = posted_data.get('last_received')
    unique_device_key = posted_data.get('device_key')
    debugFileLog.info("get_screen_data device_key is %s last_received is %s " % (unique_device_key, last_received))
    last_received_datetime = default_string_to_datetime(last_received)
    try:
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(days=nof_days)
        screen = Screen.objects.get(unique_device_key__activation_key=unique_device_key)
        # Update the screen status saying that it is active
        screen.update_status()
        if date_changed(last_received_datetime):
            schedule_ids_list = ScheduleScreens.objects.filter(
                screen=screen, schedule__deleted=False).values_list('schedule_id', flat=True)
            is_modified = True
        else:
            # Include deleted schedules as well by not checking the deleted flag
            schedule_screens = ScheduleScreens.objects.filter(
                screen=screen)
            schedule_screens_updated = schedule_screens.filter(
                schedule__last_updated_time__gte=last_received_datetime)
            if schedule_screens_updated:
                schedule_ids_list = schedule_screens.filter(schedule__deleted=False).values_list(
                    'schedule_id', flat=True).distinct()
                is_modified = True
            else:
                schedule_ids_list = []
                is_modified = False
        if schedule_ids_list:
            schedule_panes = SchedulePane.objects.filter(schedule_id__in=schedule_ids_list). \
                order_by('-schedule__last_updated_time')
        else:
            schedule_panes = []
        if schedule_panes:
            screen_data_json = screen_schedule_data(schedule_panes, start_time, end_time)
            campaigns_json = {'campaigns': screen_data_json, 'is_modified': True}
        else:
            campaigns_json = {'campaigns': [], 'is_modified': is_modified}
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
        fcm_device, created = FcmDevice.objects.get_or_create(reg_id=reg_id,
                                                              defaults={'dev_id': dev_id, 'is_active': True})
        screen = Screen.objects.get(unique_device_key__activation_key=dev_id)
        screen.fcm_device = fcm_device
        screen.save()
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
        schedule_screens = ScheduleScreens.objects.filter(screen__in=screens, schedule__deleted=False)
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
        success = False
        errors = str(e)
        return ajax_response(success=success, errors=errors)
