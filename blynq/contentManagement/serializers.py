from django.core.serializers.python import Serializer

from customLibrary.views_lib import mail_exception


def default_content_serializer(query_set, fields=('title', 'document', 'content_type', 'content_id', 'is_folder',
                                                  'duration', 'playlist_id', 'playlist_item_id')):
    return ContentSerializer().serialize(query_set, fields=fields, use_natural_foreign_keys=True)


class ContentSerializer(Serializer):
    def end_object(self, obj):
        try:
            self._current['content_id'] = obj._get_pk_val()
            self._current['thumbnail'] = obj.thumbnail_url
            if 'document' in self.selected_fields:
                self._current['url'] = obj.get_url()
                del self._current['document']
            if 'playlist_id' in self.selected_fields:
                self._current['playlist_id'] = obj.playlist_id
            if 'playlist_item_id' in self.selected_fields:
                self._current['playlist_item_id'] = obj.playlist_item_id
            if obj.is_widget:
                self._current['widget_text'] = obj.widget_text
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)
