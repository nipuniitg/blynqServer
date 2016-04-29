import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.python import Serializer

from contentManagement.models import Content
from playlistManagement.models import PlaylistItems


def playlist_dict(playlist, only_files=False):
    playlist_items = FlatJsonSerializer().get_playlist_items(playlist, only_files=only_files)
    playlist_dictionary = {'playlist_id': playlist.playlist_id, 'playlist_title': playlist.playlist_title,
                     'playlist_items': playlist_items}
    return playlist_dictionary


class FlatJsonSerializer(Serializer):
    # Ref : http://stackoverflow.com/questions/15453072/django-serializers-to-json-custom-json-output-format

    def get_screens(self, obj):
        values = obj.screen_set.all()
        screens = []
        for value in values:
            screens.append({'screen_id': value.screen_id, 'screen_name': value.screen_name,
                            'screen_size': value.screen_size, 'resolution': value.resolution,
                            'aspect_ratio':value.aspect_ratio, 'address': value.address})
        return screens

    def get_groups(self, obj):
        values = obj.groups.all()
        groups = []
        for value in values:
            groups.append({'group_id':value.group_id, 'group_name': value.group_name})
        return groups

    def add_content_fields(self, obj, data, fields=None):
        if fields == None:
            fields = self.selected_fields
        for field in fields:
            if field == 'content_id':
                data['content_id'] = obj.content_id
            if field == 'document':
                if obj.is_folder:
                    # TODO: Keep the url as the path to the default folder icon
                    data['url'] = ''
                else:
                    data['url'] = obj.document.url
            if field == 'title':
                data['title'] = obj.title
            if field == 'is_folder':
                data['is_folder'] = obj.is_folder
        return data

    def get_playlist_items(self, obj, only_files=False):
        playlist_items = PlaylistItems.objects.filter(playlist=obj).order_by('-position_index')
        contents = []
        content_fields=('title', 'document', 'content_id', 'is_folder')
        for playlist_item in playlist_items:
            if only_files and playlist_item.content.is_folder:
                continue
            data = {}
            data = self.add_content_fields(playlist_item.content, data, content_fields)
            data['playlist_item_id'] = playlist_item.playlist_item_id
            data['display_time'] = playlist_item.display_time
            contents.append(data)
        return contents

    def add_playlist_items(self, obj, data):
        for field in self.selected_fields:
            if field == 'playlist_id':
                data['playlist_id'] = obj.playlist_id
            if field == 'playlist_items':
                data['playlist_items'] = self.get_playlist_items(obj)
        return data

    def add_screen_and_group_fields(self, obj, data):
        for field in self.selected_fields:
            if field == 'screen':
                screens = self.get_screens(obj)
                data['screens'] = screens
            if field == 'groups':
                groups = self.get_groups(obj)
                data['groups'] = groups
            # field_id is not showing up in the serialized data, so adding it manually
            if field == 'group_id':
                data['group_id'] = obj.pk
            if field == 'screen_id':
                data['screen_id'] = obj.pk
            if field == 'status':
                data['status'] = obj.status.status_name
        return data

    def get_dump_object(self, obj):
        data = self._current
        # if not self.selected_fields or 'pk' in self.selected_fields:
        if not self.selected_fields:
            return data
        data = self.add_screen_and_group_fields(obj, data)
        data = self.add_content_fields(obj, data)
        data = self.add_playlist_items(obj, data)
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
