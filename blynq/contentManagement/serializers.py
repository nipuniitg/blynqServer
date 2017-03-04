from django.core.serializers.python import Serializer

from customLibrary.views_lib import mail_exception, debugFileLog


def default_content_serializer(query_set, fields=('title', 'document', 'content_type', 'content_id', 'is_folder',
                                                  'duration')):
    return ContentSerializer().serialize(query_set, fields=fields, use_natural_foreign_keys=True)


class ContentSerializer(Serializer):
    def end_object(self, obj):
        try:
            self._current['content_id'] = obj._get_pk_val()
            self._current['thumbnail'] = obj.thumbnail_url
            if 'document' in self.selected_fields:
                self._current['url'] = obj.get_url()
                del self._current['document']
            try:
                if obj.is_fb_widget:
                    self._current['url'] = obj.get_url() + str(obj.content_id)
                    self._current['no_of_posts'] = obj.fbwidget.no_of_posts
                    self._current['post_duration'] = obj.fbwidget.post_duration
                    self._current['fb_page_url'] = obj.fbwidget.fb_page_url
            except Exception as e:
                debugFileLog.error('Error while accessing fbwidget')
                debugFileLog.exception(e)
            if obj.is_text_scroll_widget:
                self._current['widget_text'] = obj.widget_text
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)
