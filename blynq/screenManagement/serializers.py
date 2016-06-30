from django.core.serializers.python import Serializer

from screenManagement.models import GroupScreens


class GroupScreensSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        self._current['group_screen_id'] = obj._get_pk_val()
        if 'group' in self.selected_fields:
            json_data = GroupSerializer().serialize([obj.group], fields=('group_id', 'group_name'))
            self.add_dict_to_current(json_data)
            del self._current['group']
        if 'screen' in self.selected_fields:
            json_data = ScreenSerializer().serialize([obj.screen],
                                                     fields=('screen_name', 'screen_size', 'aspect_ratio', 'resolution',
                                                             'address', 'city', 'screen_id'),
                                                     use_natural_foreign_keys=True)
            self.add_dict_to_current(json_data)
            del self._current['screen']
        self.objects.append(self._current)


class ScreenSerializer(Serializer):
    def end_object( self, obj ):
        self._current['screen_id'] = obj._get_pk_val()
        if 'groups' in self.selected_fields:
            group_screens = GroupScreens.objects.filter(screen=obj)
            self._current['groups'] = GroupScreensSerializer().serialize(
                group_screens, fields=('group_screen_id', 'group'))
        self.objects.append( self._current )


class GroupSerializer(Serializer):
    def end_object(self, obj):
        self._current['group_id'] = obj._get_pk_val()
        if 'screens' in self.selected_fields:
            group_screens = GroupScreens.objects.filter(group=obj)
            self._current['screens'] = GroupScreensSerializer().serialize(group_screens, fields=('group_screen_id',
                                                                                                 'screen'))
        self.objects.append(self._current)