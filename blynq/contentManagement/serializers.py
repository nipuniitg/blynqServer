from django.core.serializers.python import Serializer

from blynq import settings


def default_content_serializer(query_set, fields=('title', 'document', 'content_type', 'content_id', 'is_folder')):
    return ContentSerializer().serialize(query_set, fields=fields, use_natural_foreign_keys=True)


class ContentSerializer(Serializer):
    def end_object(self, obj):
        self._current['content_id'] = obj._get_pk_val()
        if 'document' in self.selected_fields:
            if obj.document:
                self._current['url'] = settings.MEDIA_HOST + obj.document.url
            else:
                self._current['url'] = obj.url
            del self._current['document']
        if obj.is_widget:
            self._current['widget_text'] = obj.widget_text
        self.objects.append(self._current)


# def default_widget_serializer(querySet):
#     return WidgetSerializer().serialize(querySet, fields=('title', 'text', 'type', 'widget_id'),
#                                         use_natural_foreign_keys=True)
#
#
# class WidgetSerializer(Serializer):
#     def end_object(self, obj):
#         self._current['widget_id'] = obj._get_pk_val()
#         if 'text' in self.selected_fields:
#             self._current['url'] = obj.text
#         self.objects.append(self._current)