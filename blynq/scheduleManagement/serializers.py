from django.core.serializers.python import Serializer

from customLibrary.views_lib import get_ist_date_str, get_ist_time_str
from playlistManagement.serializers import PlaylistSerializer
from scheduleManagement.models import SchedulePlaylists, ScheduleScreens
from screenManagement.serializers import ScreenSerializer


class SchedulePlaylistsSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        self._current['schedule_playlist_id'] = obj._get_pk_val()
        if 'playlist' in self.selected_fields:
            json_data = PlaylistSerializer().serialize([obj.playlist], fields=('playlist_id', 'playlist_title',
                                                                               'playlist_items') )
            self.add_dict_to_current(json_data)
            del self._current['playlist']
        self.objects.append(self._current)


class ScheduleScreensSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        self._current['schedule_screen_id'] = obj._get_pk_val()
        if 'screen' in self.selected_fields:
            json_data = ScreenSerializer().serialize([obj.screen],
                                                     fields=('screen_id', 'status', 'groups', 'address', 'city',
                                                             'screen_size', 'resolution', 'screen_name'),
                                                     use_natural_foreign_keys=True)
            self.add_dict_to_current(json_data)
            del self._current['screen']
        if 'group' in self.selected_fields:
            json_data = ScreenSerializer().serialize([obj.group],
                                                     fields=('group_id', 'group_name', 'description', 'screen'))
            self.add_dict_to_current(json_data)
            del self._current['group']
        self.objects.append(self._current)


def default_timeline():
    return {'is_always': True, 'recurrence_absolute': False, 'all_day': True, 'start_date':None,
            'end_recurring_period': None, 'start_time': None, 'end_time': None, 'frequency':None, 'interval': None,
            'byweekday': None, 'bymonthday': None, 'byweekno': None }


def get_schedule_timeline(schedule):
    schedule_screens = ScheduleScreens.objects.filter(schedule=schedule)
    event_json = {}
    if schedule_screens:
        event = schedule_screens[0].event
        if event:
            event_json['is_always'] = schedule.is_always
            event_json['recurrence_absolute'] = schedule.recurrence_absolute
            event_json['all_day'] = schedule.all_day
            event_json['start_date'] = get_ist_date_str(event.start) if event.start else None
            if event.end_recurring_period:
                event_json['end_recurring_period'] = get_ist_date_str(utc_datetime=event.end_recurring_period)
            else:
                event_json['end_recurring_period'] = None
            event_json['start_time'] = get_ist_time_str(utc_datetime=event.start) if event.start else None
            event_json['end_time'] = get_ist_time_str(utc_datetime=event.end) if event.end else None
            rule = event.rule
            params = rule.get_params() if rule else {}
            event_json['frequency'] = rule.frequency if rule else None
            event_json['interval'] = params.get('interval')
            event_json['byweekday'] = params.get('byweekday')
            event_json['bymonthday'] = params.get('bymonthday')
            event_json['byweekno'] = params.get('byweekno')
            return event_json
        print "Event doesn't exist for the schedule"
    else:
        print "No screens added for this schedule"
    return default_timeline()



class ScheduleSerializer(Serializer):
    def end_object(self, obj):
        self._current['schedule_id'] = obj._get_pk_val()
        if 'schedule_playlists' in self.selected_fields:
            schedule_playlists = SchedulePlaylists.objects.filter(schedule=obj)
            json_data = SchedulePlaylistsSerializer().serialize(
                schedule_playlists, fields=('schedule_playlist_id','playlist'))
            self._current['schedule_playlists'] = json_data
        if 'schedule_screens' in self.selected_fields:
            schedule_screens = ScheduleScreens.objects.filter(schedule=obj, group__isnull=True)
            json_data = ScheduleScreensSerializer().serialize(
                schedule_screens, fields=('schedule_screen_id','screen'))
            self._current['schedule_screens'] = json_data
        if 'schedule_groups' in self.selected_fields:
            schedule_screens = ScheduleScreens.objects.filter(schedule=obj, group__isnull=False)
            json_data = ScheduleScreensSerializer().serialize(
                schedule_screens, fields=('schedule_screen_id','group'))
            self._current['schedule_groups'] = json_data
        if 'timeline' in self.selected_fields:
            self._current['timeline'] = get_schedule_timeline(obj)
        self.objects.append(self._current)