from django.core.serializers.python import Serializer

from customLibrary.views_lib import get_ist_date_str, get_ist_time_str, debugFileLog
from playlistManagement.serializers import PlaylistSerializer
from scheduleManagement.models import SchedulePlaylists, ScheduleScreens, SchedulePane
from layoutManagement.models import LayoutPane
from screenManagement.serializers import ScreenSerializer, GroupSerializer
from layoutManagement.serializers import LayoutPaneSerializer, LayoutSerializer, default_layout_serializer, \
    default_layout_pane_serializer


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


class SchedulePaneSerializer(Serializer):
    def end_object(self, obj):
        self._current['schedule_pane_id'] = obj._get_pk_val()
        if 'schedule_playlists' in self.selected_fields:
            schedule_playlists = SchedulePlaylists.objects.filter(schedule_pane=obj)
            json_data = SchedulePlaylistsSerializer().serialize(
                schedule_playlists, fields=('schedule_playlist_id','playlist'))
            self._current['schedule_playlists'] = json_data
        if 'layout_pane' in self.selected_fields:
            if obj.layout_pane:
                json_data = default_layout_pane_serializer([obj.layout_pane])
                self._current['layout_pane'] = json_data[0]
            else:
                self._current['layout_pane'] = {}
        if 'timeline' in self.selected_fields:
            self._current['timeline'] = get_schedule_timeline(obj)
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
            json_data = GroupSerializer().serialize([obj.group],
                                                    fields=('group_id', 'group_name', 'description', 'screen'))
            self.add_dict_to_current(json_data)
            del self._current['group']
        self.objects.append(self._current)


def default_timeline():
    return {'is_always': True, 'recurrence_absolute': False, 'all_day': True, 'start_date': None,
            'end_recurring_period': None, 'start_time': None, 'end_time': None, 'frequency': None, 'interval': None,
            'byweekday': None, 'bymonthday': None, 'byweekno': None }


def get_schedule_timeline(schedule_pane):
    event_json = {}
    event = schedule_pane.event
    if event:
        event_json['is_always'] = schedule_pane.is_always
        event_json['recurrence_absolute'] = schedule_pane.recurrence_absolute
        event_json['all_day'] = schedule_pane.all_day
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
    debugFileLog.error("Event doesn't exist for the schedule")
    return default_timeline()


class ScheduleSerializer(Serializer):
    def end_object(self, obj):
        self._current['schedule_id'] = obj._get_pk_val()
        if 'schedule_screens' in self.selected_fields:
            schedule_screens = ScheduleScreens.objects.filter(schedule=obj, group__isnull=True)
            json_data = ScheduleScreensSerializer().serialize(
                schedule_screens, fields=('schedule_screen_id','screen'))
            self._current['schedule_screens'] = json_data
        if 'schedule_groups' in self.selected_fields:
            schedule_groups = ScheduleScreens.objects.filter(schedule=obj, screen__isnull=True, group__isnull=False)
            json_data = ScheduleScreensSerializer().serialize(
                schedule_groups, fields=('schedule_screen_id','group'))
            self._current['schedule_groups'] = json_data
        if 'layout' in self.selected_fields:
            if obj.layout:
                json_data = default_layout_serializer([obj.layout])
                self._current['layout'] = json_data[0]
            else:
                self._current['layout'] = {}
        if 'schedule_panes' in self.selected_fields:
            schedule_panes = SchedulePane.objects.filter(schedule=obj)
            json_data = SchedulePaneSerializer().serialize(schedule_panes,
                                                           fields=('schedule_pane_id', 'schedule_playlists',
                                                                   'layout_pane', 'timeline'))
            self._current['schedule_panes'] = json_data
        self.objects.append(self._current)


def default_schedule_serializer(querySet):
    return ScheduleSerializer().serialize(querySet, fields=('schedule_id', 'schedule_title',
                                                            'schedule_panes', 'is_split', 'layout',
                                                            'schedule_screens', 'schedule_groups'))