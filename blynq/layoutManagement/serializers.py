from django.core.serializers.python import Serializer

from layoutManagement.models import LayoutPane


class LayoutPaneSerializer(Serializer):
    def end_object(self, obj):
        self._current['layout_pane_id'] = obj._get_pk_val()
        self.objects.append(self._current)


class LayoutSerializer(Serializer):
    def end_object(self, obj):
        self._current['layout_id'] = obj._get_pk_val()
        if 'layout_panes' in self.selected_fields:
            layout_panes = LayoutPane.objects.filter(layout=obj)
            self._current['layout_panes'] = LayoutPaneSerializer().serialize(layout_panes,
                                                                             fields=('layout_pane_id', 'title'))
        self.objects.append(self._current)
