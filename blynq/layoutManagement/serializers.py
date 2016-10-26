from django.core.serializers.python import Serializer

from layoutManagement.models import LayoutPane
from screenManagement.serializers import AspectRatioSerializer


def default_layout_pane_serializer(querySet):
    return LayoutPaneSerializer().serialize(querySet, fields=('layout_pane_id', 'title', 'left_margin', 'top_margin',
                                                              'z_index', 'width', 'height'))


class LayoutPaneSerializer(Serializer):
    def end_object(self, obj):
        self._current['layout_pane_id'] = obj._get_pk_val()
        self.objects.append(self._current)


def default_layout_serializer(querySet):
    return LayoutSerializer().serialize(querySet, fields=('layout_id', 'title', 'layout_panes', 'aspect_ratio'))


class LayoutSerializer(Serializer):
    def end_object(self, obj):
        self._current['layout_id'] = obj._get_pk_val()
        if 'layout_panes' in self.selected_fields:
            layout_panes = LayoutPane.objects.filter(layout=obj)
            self._current['layout_panes'] = default_layout_pane_serializer(layout_panes)
        if 'aspect_ratio' in self.selected_fields:
            if obj.aspect_ratio:
                self._current['aspect_ratio'] = AspectRatioSerializer().serialize([obj.aspect_ratio])[0]
            else:
                self._current['aspect_ratio'] = {}
        self.objects.append(self._current)
