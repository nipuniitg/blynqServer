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
        if 'content_type' in self.selected_fields:
            if obj.content_type and (obj.content_type.file_type == 'file/audio/mpeg' or obj.content_type.file_type == 'file/audio/mp3'):
                self._current['content_type'] = 'file/video/mp4'
        self.objects.append(self._current)
