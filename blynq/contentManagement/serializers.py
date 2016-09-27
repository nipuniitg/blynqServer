from django.core.serializers.python import Serializer

from blynq import settings


def default_content_serializer(query_set, fields=('title', 'document', 'content_type', 'content_id', 'is_folder',
                                                  'duration')):
    return ContentSerializer().serialize(query_set, fields=fields, use_natural_foreign_keys=True)


class ContentSerializer(Serializer):
    def end_object(self, obj):
        self._current['content_id'] = obj._get_pk_val()
        self._current['thumbnail'] = obj.thumbnail
        if 'document' in self.selected_fields:
            self._current['url'] = obj.get_url()
            del self._current['document']
        if obj.is_widget:
            self._current['widget_text'] = obj.widget_text
        self.objects.append(self._current)
