import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.python import Serializer


class FlatJsonSerializer(Serializer):
    # Ref : http://stackoverflow.com/questions/15453072/django-serializers-to-json-custom-json-output-format

    def get_screens(self, obj):
        values = obj.screen_set.all()
        screens = []
        for value in values:
            screens.append({'screen_id': value.screen_id, 'screen_name': value.screen_name})
        return screens

    def get_groups(self, obj):
        values = obj.groups.all()
        groups = []
        for value in values:
            groups.append({'group_id':value.group_id, 'group_name': value.group_name})
        return groups

    def get_dump_object(self, obj):
        data = self._current
        # if not self.selected_fields or 'pk' in self.selected_fields:
        if not self.selected_fields:
            return data
        for field in self.selected_fields:
            if field == 'screen':
                screens = self.get_screens(obj)
                data['screens'] = screens
            if field == 'groups':
                groups = self.get_groups(obj)
                data['groups'] = groups
            if field == 'group_id':
                data['group_id'] = obj.pk
            if field == 'screen_id':
                data['screen_id'] = obj.pk
            if field == 'status':
                data['status'] = obj.status.status_name
        return data

    def end_object(self, obj):
        if not self.first:
            self.stream.write(', ')
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=DjangoJSONEncoder)
        self._current = None

    def start_serialization(self):
        self.stream.write("[")

    def end_serialization(self):
        self.stream.write("]")

    def getvalue(self):
        return super(Serializer, self).getvalue()
