from django.core.serializers.python import Serializer

from contentManagement.serializers import ContentSerializer
from playlistManagement.models import PlaylistItems


class PlaylistItemsSerializer(Serializer):
    def add_dict_to_current(self, json_data):
        for each_dict in json_data:
            self._current.update(each_dict)

    def end_object(self, obj):
        self._current['playlist_item_id'] = obj._get_pk_val()
        if 'content' in self.selected_fields:
            json_data = ContentSerializer().serialize([obj.content], fields=('title', 'document', 'content_type',
                                                                             'content_id', 'is_folder'))
            self.add_dict_to_current(json_data)
            del self._current['content']
        self.objects.append(self._current)


class PlaylistSerializer(Serializer):
    def end_object(self, obj):
        self._current['playlist_id'] = obj._get_pk_val()
        if 'playlist_items' in self.selected_fields:
            playlist_items_data = PlaylistItems.objects.filter(playlist=obj)
            self._current['playlist_items'] = PlaylistItemsSerializer().serialize(
                playlist_items_data,fields=('playlist_item_id', 'display_time', 'content'))
        self.objects.append(self._current)