from django.core.serializers.python import Serializer

from customLibrary.views_lib import mail_exception
from playlistManagement.serializers import PlaylistSerializer
from screenManagement.serializers import GroupSerializer, default_screen_serializer
from layoutManagement.serializers import default_layout_serializer, default_layout_pane_serializer


class SchedulePlaylistsSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        try:
            self._current['schedule_playlist_id'] = obj._get_pk_val()
            if 'playlist' in self.selected_fields:
                json_data = PlaylistSerializer().serialize([obj.playlist], fields=('playlist_id', 'playlist_title',
                                                                                   'playlist_items', 'playlist_type'))
                self.add_dict_to_current(json_data)
                del self._current['playlist']
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


class SchedulePaneSerializer(Serializer):
    def end_object(self, obj):
        try:
            self._current['schedule_pane_id'] = obj._get_pk_val()
            if 'schedule_playlists' in self.selected_fields:
                schedule_playlists = obj.get_schedule_playlists_manager.all().order_by('position_index')
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
                self._current['timeline'] = obj.get_schedule_timeline()
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


class ScheduleScreensSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        try:
            self._current['schedule_screen_id'] = obj._get_pk_val()
            if 'screen' in self.selected_fields:
                json_data = default_screen_serializer([obj.screen])
                self.add_dict_to_current(json_data)
                del self._current['screen']
            if 'group' in self.selected_fields:
                json_data = GroupSerializer().serialize([obj.group],
                                                        fields=('group_id', 'group_name', 'description', 'screen'))
                self.add_dict_to_current(json_data)
                del self._current['group']
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


class ScheduleSerializer(Serializer):
    def end_object(self, obj):
        try:
            self._current['schedule_id'] = obj._get_pk_val()
            if 'schedule_screens' in self.selected_fields:
                schedule_screens = obj.get_schedule_screens_manager.filter(group__isnull=True)
                json_data = ScheduleScreensSerializer().serialize(
                    schedule_screens, fields=('schedule_screen_id','screen'))
                self._current['schedule_screens'] = json_data
            if 'schedule_groups' in self.selected_fields:
                schedule_groups = obj.get_schedule_screens_manager.filter(screen__isnull=True, group__isnull=False)
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
                schedule_panes = obj.get_schedule_pane_manager.all()
                json_data = SchedulePaneSerializer().serialize(schedule_panes,
                                                               fields=('schedule_pane_id', 'schedule_playlists',
                                                                       'layout_pane', 'timeline', 'mute_audio'))
                self._current['schedule_panes'] = json_data
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


def default_schedule_serializer(querySet):
    return ScheduleSerializer().serialize(querySet, fields=('schedule_id', 'schedule_title', 'schedule_description',
                                                            'schedule_panes', 'is_split', 'layout',
                                                            'schedule_screens', 'schedule_groups'))