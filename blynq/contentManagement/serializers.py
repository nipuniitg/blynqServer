from django.core.serializers.python import Serializer

from blynq import settings


class ContentSerializer(Serializer):
    def end_object(self, obj):
        self._current['content_id'] = obj._get_pk_val()
        if 'document' in self.selected_fields:
            if obj.is_folder:
                # TODO: Keep the url as the path to the default folder icon
                self._current['url'] = ''
            else:
                self._current['url'] = settings.MEDIA_HOST + obj.document.url
            del self._current['document']
        self.objects.append(self._current)
