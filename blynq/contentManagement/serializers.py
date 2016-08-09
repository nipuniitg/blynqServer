from django.core.serializers.python import Serializer

from blynq import settings


class ContentSerializer(Serializer):
    def end_object(self, obj):
        self._current['content_id'] = obj._get_pk_val()
        if 'document' in self.selected_fields:
            if obj.document:
                self._current['url'] = settings.MEDIA_HOST + obj.document.url
            else:
                self._current['url'] = obj.url
            del self._current['document']
        self.objects.append(self._current)


def default_widget_serializer(querySet):
    return WidgetSerializer().serialize(querySet, fields=('title', 'text', 'type', 'widget_id'),
                                        use_natural_foreign_keys=True)


class WidgetSerializer(Serializer):
    def end_object(self, obj):
        self._current['widget_id'] = obj._get_pk_val()
        if 'text' in self.selected_fields:
            self._current['url'] = obj.text
        self.objects.append(self._current)