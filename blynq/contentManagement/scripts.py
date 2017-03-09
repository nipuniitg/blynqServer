from contentManagement.models import Content, ScrollTextWidget
from customLibrary.views_lib import debugFileLog

__author__ = 'nipun'


def convert_existing_scroll_widgets():
    contents = Content.objects.filter(widget_text__isnull=False)
    for content in contents:
        try:
            scroll_text_widget = ScrollTextWidget.objects.create(content=content, widget_text=content.widget_text)
        except Exception as e:
            debugFileLog.error('Unable to create ScrollTextWidget for %s' % str(content.content_id))
        print '%s converted successful' % content.title
