from datetime import timedelta, datetime
from django.shortcuts import render

# Create your views here.
from contentManagement.models import Content
from customLibrary.views_lib import get_userdetails, generate_utc_datetime, get_ist_date_str, obj_to_json_response, \
    debugFileLog, string_to_dict, string_to_date, date_to_string
from playlistManagement.models import Playlist
from reports.models import ScreenAnalytics, MediaAnalytics
from screenManagement.models import Screen


def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def date_time_filters(filter_set):
    start_date_str = filter_set.get('start_date')
    start_time_str = filter_set.get('start_time')
    start_time_str = start_time_str if start_time_str else "00:00"
    start_datetime = generate_utc_datetime(start_date_str, start_time_str)
    end_date_str = filter_set.get('end_date')
    end_time_str = filter_set.get('end_time')
    end_time_str = end_time_str if end_time_str else "23:59"
    start_date_end_time = generate_utc_datetime(start_date_str, end_time_str)
    time_difference = start_date_end_time - start_datetime
    end_date_start_time = generate_utc_datetime(end_date_str, start_time_str)
    end_date = end_date_start_time.date() + timedelta(days=1)
    return start_datetime, end_date, time_difference


def intersection_time(event1_start, event1_end, event2_start, event2_end):
    """
    :param event1_start: start datetime of event1
    :param event1_end: end datetime of event1
    :param event2_start: start datetime of event2
    :param event2_end: end datetime of even2
    Four sets of times should be checked, e1 - s1 ;  e2 - s2 ; e1 - s2 ; e2 - s1
    :return: intersection time in seconds
    """
    delta = (event1_end - event1_start).seconds
    new_delta = (event2_end - event2_start).seconds
    if new_delta < delta:
        delta = new_delta
    new_delta = event1_end - event2_start
    if new_delta < delta:
        delta = new_delta
    new_delta = event2_end - event1_start
    if new_delta < delta:
        delta = new_delta
    return delta


def screen_filter(filter_set, user_details):
    all_screens = filter_set.get('all_screens')
    screen_ids = []
    if all_screens:
        screen_ids = Screen.get_user_relevant_objects(user_details=user_details).values_list('screen_id', flat=True)
    else:
        screen_objects = filter_set.get('screens')
        if screen_objects:
            screen_ids = (item['screen_id'] for item in screen_objects)
    return screen_ids


def playlist_filter(filter_set, user_details):
    playlist_ids = []
    all_playlists = filter_set.get('all_playlists')
    if all_playlists:
        playlist_ids = Playlist.get_user_relevant_objects(user_details=user_details).values_list('playlist_id', flat=True)
    else:
        playlist_objects = filter_set.get('playlists')
        if playlist_objects:
            playlist_ids = (item['playlist_id'] for item in playlist_objects)
    return playlist_ids


def content_filter(filter_set, user_details):
    content_ids = []
    all_content_files = filter_set.get('all_content_files')
    if all_content_files:
        content_ids = Content.get_user_relevant_objects(user_details=user_details).values_list('content_id', flat=True)
    else:
        content_objects = filter_set.get('content_files')
        if content_objects:
            content_ids = (item['content_id'] for item in content_objects)
    return content_ids


def screen_reports(request):
    # Input filter_set
    # start_date, end_date, start_time, end_time : ist datetime
    # all_screens : bool, screens : array of screen objects
    # output : For each screen: screen object, time_active (seconds),
    #       total_time (end_date - start_date + 1)*(end_time - start_time)
    date_str_list, time_active_list, pie_chart_data, table_data = ([] for i in range(4))
    line_chart_data = {'date_str': [], 'time_active': []}
    json_dict = {'line_chart_data': line_chart_data, 'pie_chart_data': pie_chart_data, 'table_data': table_data }
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        filter_set = posted_data.get('filterset')
        screen_ids = screen_filter(filter_set, user_details)
        start_datetime, end_date, time_difference = date_time_filters(filter_set=filter_set)
        total_days = (end_date - start_datetime.date()).days
        total_time_requested = total_days * time_difference.seconds
        if end_date < start_datetime.date():
            return obj_to_json_response(json_dict)
        all_screens_dict = {}
        total_time_active = 0
        screen_objects = Screen.get_user_relevant_objects(user_details).filter(screen_id__in=screen_ids)
        for obj in screen_objects:
            all_screens_dict[str(obj.screen_id)] = {'screen_id': obj.screen_id, 'screen_name': obj.screen_name,
                                                    'time_active': 0, 'total_time_requested': total_time_requested}
        for single_date in date_range(start_date=start_datetime.date(), end_date=end_date):
            start = datetime.combine(single_date, start_datetime.time())
            end = start + time_difference
            date_str = get_ist_date_str(start)
            date_str_list.append(date_str)
            screen_analytics = ScreenAnalytics.objects.exclude(
                screen_id__in=screen_ids, session_start_time__gte=end,
                session_end_time__lte=start_datetime).order_by('screen_id')
            date_active_time = 0    # active_time of all_screens in a single date
            for obj in screen_analytics:
                time_active = intersection_time(start_datetime, end, obj.session_start_time, obj.session_end_time)
                date_active_time += time_active
                total_time_active += time_active
                screen_id_key = str(obj.screen_id)
                if all_screens_dict.get(screen_id_key) and all_screens_dict[screen_id_key]['time_active']:
                    all_screens_dict[str(obj.screen_id)]['time_active'] += time_active
                else:
                    all_screens_dict[str(obj.screen_id)] = {
                        'screen_id': obj.screen_id, 'screen_name': obj.screen.screen_name,
                        'time_active': time_active, 'total_time_requested': total_time_requested}
            time_active_list.append(date_active_time/3600.0)    # converting into hours
        if total_time_requested >= total_time_active:
            pie_chart_data = [total_time_active, total_time_requested-total_time_active]
        table_data = all_screens_dict.values()
        line_chart_data = {'date_str': date_str_list, 'time_active': time_active_list}
        json_dict = {'line_chart_data': line_chart_data, 'pie_chart_data': pie_chart_data, 'table_data': table_data}
    except Exception as e:
        debugFileLog.exception(e)
    return obj_to_json_response(json_dict)


def playlist_reports(request):
    date_str_list, time_played_list, table_data = ([] for i in range(3))
    line_chart_data = {'date_str': [], 'time_played': []}
    json_dict = {'line_chart_data': line_chart_data, 'table_data': table_data }
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        filter_set = posted_data.get('filterset')
        # Input filter_set
        # start_date, end_date, start_time, end_time : ist datetime
        # all_screens : bool, screens : array of screen objects
        # all_playlists : bool, playlists: array of playlist objects
        # output : line_chart_data and table_data
        screen_ids = screen_filter(filter_set=filter_set, user_details=user_details)
        playlist_ids = playlist_filter(filter_set=filter_set, user_details=user_details)
        start_date = string_to_date(filter_set.get('start_date'))
        end_date = string_to_date(filter_set.get('end_date'))
        if end_date <= start_date:
            return obj_to_json_response(json_dict)
        all_screens_dict = {}
        screen_objects = Screen.get_user_relevant_objects(user_details).filter(screen_id__in=screen_ids)
        for obj in screen_objects:
            all_screens_dict[str(obj.screen_id)] = {'screen_id': obj.screen_id, 'screen_name': obj.screen_name}
        all_playlists_dict = {}
        playlist_objects = Playlist.get_user_relevant_objects(user_details).filter(playlist_id__in=playlist_ids)
        for obj in playlist_objects:
            all_playlists_dict[str(obj.playlist_id)] = {
                'playlist_id': obj.playlist_id, 'playlist_title': obj.playlist_title, 'num_of_repetitions': 0,
                'time_played': 0, 'screens_played': []}
        for single_date in date_range(start_date=start_date, end_date=end_date+timedelta(days=1)):
            date_str = date_to_string(single_date)
            date_str_list.append(date_str)
            time_played_each_day = 0
            media_analytics = MediaAnalytics.objects.filter(screen_id__in=screen_ids, playlist_id__in=playlist_ids,
                                                            date=single_date)
            for obj in media_analytics:
                playlist_dict = all_playlists_dict[str(obj.playlist_id)]
                time_played_each_day += obj.total_time
                playlist_dict['num_of_repetitions'] += obj.count
                playlist_dict['time_played'] += obj.total_time
                if all_screens_dict[str(obj.screen_id)] not in playlist_dict['screens_played']:
                    playlist_dict['screens_played'].append(all_screens_dict[str(obj.screen_id)])
            time_played_list.append(time_played_each_day/60.0) # converting into minutes
        table_data = all_playlists_dict.values()
        line_chart_data = {'date_str': date_str_list, 'time_played': time_played_list}
        json_dict = {'line_chart_data': line_chart_data, 'table_data': table_data}
    except Exception as e:
        debugFileLog.exception(e)
    return obj_to_json_response(json_dict)


def media_reports(request):
    date_str_list, time_played_list, table_data = ([] for i in range(3))
    line_chart_data = {'date_str': [], 'time_played': []}
    json_dict = {'line_chart_data': line_chart_data, 'table_data': table_data }
    try:
        user_details = get_userdetails(request)
        posted_data = string_to_dict(request.body)
        filter_set = posted_data.get('filterset')
        # Input filter_set
        # start_date, end_date, start_time, end_time : ist datetime
        # all_screens : bool, screens : array of screen objects
        # all_playlists : bool, playlists: array of playlist objects
        # all_content_files :  bool, content_files : array of content objects
        screen_ids = screen_filter(filter_set=filter_set, user_details=user_details)
        playlist_ids = playlist_filter(filter_set=filter_set, user_details=user_details)
        content_ids = content_filter(filter_set=filter_set, user_details=user_details)
        start_date = string_to_date(filter_set.get('start_date'))
        end_date = string_to_date(filter_set.get('end_date'))
        if end_date <= start_date:
            return obj_to_json_response(json_dict)
        all_screens_dict = {}
        screen_objects = Screen.get_user_relevant_objects(user_details).filter(screen_id__in=screen_ids)
        for obj in screen_objects:
            all_screens_dict[str(obj.screen_id)] = {'screen_id': obj.screen_id, 'screen_name': obj.screen_name}
        all_playlists_dict = {}
        playlist_objects = Playlist.get_user_relevant_objects(user_details).filter(playlist_id__in=playlist_ids)
        for obj in playlist_objects:
            all_playlists_dict[str(obj.playlist_id)] = {'playlist_id': obj.playlist_id,
                                                        'playlist_title': obj.playlist_title}
        all_content_dict = {}
        content_objects = Content.get_user_relevant_objects(user_details).filter(content_id__in=content_ids)
        for obj in content_objects:
            all_content_dict[str(obj.content_id)] = {
                'content_id': obj.content_id, 'content_title': obj.title, 'num_of_repetitions': 0,
                'time_played': 0, 'screens_played': [], 'playlists_played': []}
        for single_date in date_range(start_date=start_date, end_date=end_date+timedelta(days=1)):
            date_str = date_to_string(single_date)
            date_str_list.append(date_str)
            time_played_each_day = 0
            media_analytics = MediaAnalytics.objects.filter(screen_id__in=screen_ids, playlist_id__in=playlist_ids,
                                                            content_id__in=content_ids, date=single_date)
            for obj in media_analytics:
                content_dict = all_content_dict[str(obj.content_id)]
                time_played_each_day += obj.total_time
                content_dict['num_of_repetitions'] += obj.count
                content_dict['time_played'] += obj.total_time
                if all_screens_dict[str(obj.screen_id)] not in content_dict['screens_played']:
                    content_dict['screens_played'].append(all_screens_dict[str(obj.screen_id)])
                if all_playlists_dict[str(obj.playlist_id)] not in content_dict['playlists_played']:
                    content_dict['playlists_played'].append(all_playlists_dict[str(obj.playlist_id)])
            time_played_list.append(time_played_each_day/60.0) # converting into minutes
        table_data = all_content_dict.values()
        line_chart_data = {'date_str': date_str_list, 'time_played': time_played_list}
        json_dict = {'line_chart_data': line_chart_data, 'table_data': table_data}
    except Exception as e:
        debugFileLog.exception(e)
    return obj_to_json_response(json_dict)
