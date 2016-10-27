from django.core.serializers.python import Serializer

from customLibrary.views_lib import datetime_to_string, get_ist_datetime, wrap_try_catch, mail_exception
from screenManagement.models import GroupScreens


def default_screen_serializer(query_set, fields=('screen_id', 'screen_name', 'address', 'city', 'status', 'screen_size',
                                                 'aspect_ratio', 'resolution', 'last_active_time', 'groups')):
    return ScreenSerializer().serialize(query_set, fields=fields, use_natural_foreign_keys=True)


class GroupScreensSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        try:
            self._current['group_screen_id'] = obj._get_pk_val()
            if 'group' in self.selected_fields:
                json_data = GroupSerializer().serialize([obj.group], fields=('group_id', 'group_name'))
                self.add_dict_to_current(json_data)
                del self._current['group']
            if 'screen' in self.selected_fields:
                # groups field should not be passed for the default_screen_serializer
                json_data = default_screen_serializer(query_set=[obj.screen], fields=(
                    'screen_id', 'screen_name', 'address', 'city', 'status', 'screen_size', 'aspect_ratio', 'resolution',
                    'last_active_time'))
                self.add_dict_to_current(json_data)
                del self._current['screen']
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


class ScreenSerializer(Serializer):
    def end_object( self, obj ):
        try:
            if 'screen_id' in self.selected_fields:
                self._current['screen_id'] = obj._get_pk_val()
            if 'groups' in self.selected_fields:
                group_screens = GroupScreens.objects.filter(screen=obj)
                self._current['groups'] = GroupScreensSerializer().serialize(
                    group_screens, fields=('group_screen_id', 'group'))
            if 'status' in self.selected_fields:
                self._current['status'] = obj.current_status
            if 'last_active_time' in self.selected_fields:
                self._current['last_active_time'] = datetime_to_string(get_ist_datetime(obj.last_active_time))
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


class GroupSerializer(Serializer):
    def end_object(self, obj):
        try:
            self._current['group_id'] = obj._get_pk_val()
            if 'screens' in self.selected_fields:
                group_screens = GroupScreens.objects.filter(group=obj)
                self._current['screens'] = GroupScreensSerializer().serialize(group_screens, fields=('group_screen_id',
                                                                                                     'screen'))
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)


class AspectRatioSerializer(Serializer):
    def end_object(self, obj):
        try:
            self._current['aspect_ratio_id'] = obj._get_pk_val()
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)
