import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.python import Serializer

from blynq import settings
from contentManagement.models import Content
from customLibrary.views_lib import get_ist_date_str, get_ist_time_str
from playlistManagement.models import PlaylistItems
from scheduleManagement.models import SchedulePlaylists, ScheduleScreens
from screenManagement.models import GroupScreens


def default_timeline():
    return {'is_always': True, 'recurrence_absolute': False, 'all_day': True, 'start_date':None,
            'end_recurring_period': None, 'start_time': None, 'end_time': None, 'frequency':None, 'interval': None,
            'byweekday': None, 'bymonthday': None, 'byweekno': None }


def playlist_dict(playlist, only_files=False):
    playlist_items = FlatJsonSerializer().get_playlist_items(playlist, only_files=only_files)
    playlist_dictionary = {'playlist_id': playlist.playlist_id, 'playlist_title': playlist.playlist_title,
                     'playlist_items': playlist_items}
    return playlist_dictionary


def get_schedule_playlists(schedule):
    schedule_playlists_list = []
    schedule_playlists = SchedulePlaylists.objects.filter(schedule=schedule).order_by('position_index')
    for each_schedule_playlist in schedule_playlists:
        single_json = playlist_dict(each_schedule_playlist.playlist)
        single_json['schedule_playlist_id'] = each_schedule_playlist.schedule_playlist_id
        schedule_playlists_list.append(single_json)
    return schedule_playlists_list


def get_schedule_screens(schedule):
    schedule_screens_list = []
    schedule_screens_all = ScheduleScreens.objects.filter(schedule=schedule)
    schedule_screens = schedule_screens_all.exclude(group__isnull=False)
    for each_schedule_screen in schedule_screens:
        screen = each_schedule_screen.screen
        screen_groups = FlatJsonSerializer().get_groups(screen)
        single_json = {'screen_id': screen.screen_id, 'screen_name': screen.screen_name, 'address': screen.address,
                       'status': screen.status.status_name, 'groups': screen_groups,
                       'screen_size': screen.screen_size, 'resolution': screen.resolution,
                       'schedule_screen_id': each_schedule_screen.schedule_screen_id}
        schedule_screens_list.append(single_json)
    return schedule_screens_list


def get_schedule_groups(schedule):
    schedule_groups_list = []
    schedule_groups_all = ScheduleScreens.objects.filter(schedule=schedule)
    # Extract Groups
    schedule_groups = schedule_groups_all.filter(group__isnull=False)
    for each_schedule_group in schedule_groups:
        group = each_schedule_group.group
        group_screens = FlatJsonSerializer().get_screens(group)
        single_json = {'group_id': group.group_id, 'group_name': group.group_name,
                       'description': group.description, 'screen': group_screens,
                       'schedule_screen_id': each_schedule_group.schedule_screen_id}
        schedule_groups_list.append(single_json)
    return schedule_groups_list


def get_schedule_timeline(schedule):
    schedule_screens = ScheduleScreens.objects.filter(schedule=schedule)
    event_json = {}
    if schedule_screens:
        event = schedule_screens[0].event
        if event:
            event_json['is_always'] = schedule.is_always
            event_json['recurrence_absolute'] = schedule.recurrence_absolute
            event_json['all_day'] = schedule.all_day
            event_json['start_date'] = get_ist_date_str(event.start) if event.start else None
            if event.end_recurring_period:
                event_json['end_recurring_period'] = get_ist_date_str(utc_datetime=event.end_recurring_period)
            else:
                event_json['end_recurring_period'] = None
            event_json['start_time'] = get_ist_time_str(utc_datetime=event.start) if event.start else None
            event_json['end_time'] = get_ist_time_str(utc_datetime=event.end) if event.end else None
            rule = event.rule
            params = rule.get_params() if rule else {}
            event_json['frequency'] = rule.frequency if rule else None
            event_json['interval'] = params.get('interval')
            event_json['byweekday'] = params.get('byweekday')
            event_json['bymonthday'] = params.get('bymonthday')
            event_json['byweekno'] = params.get('byweekno')
            return event_json
        print "Event doesn't exist for the schedule"
    else:
        print "No screens added for this schedule"
    return default_timeline()


def schedule_dict(schedule):
    schedule_dictionary = {'schedule_id': schedule.schedule_id, 'schedule_title': schedule.schedule_title,
                           'schedule_playlists': get_schedule_playlists(schedule),
                           'schedule_screens': get_schedule_screens(schedule),
                           'schedule_groups': get_schedule_groups(schedule),
                           'timeline': get_schedule_timeline(schedule), }
    return schedule_dictionary


class FlatJsonSerializer(Serializer):
    # Ref : http://stackoverflow.com/questions/15453072/django-serializers-to-json-custom-json-output-format

    def get_screens(self, obj):
        group_screens = GroupScreens.objects.filter(group=obj)
        screens = []
        for each_group_screen in group_screens:
            screen = each_group_screen.screen
            screens.append({'group_screen_id': each_group_screen.group_screen_id, 'screen_id': screen.screen_id,
                            'screen_name': screen.screen_name, 'screen_size': screen.screen_size,
                            'resolution': screen.resolution, 'aspect_ratio':screen.aspect_ratio,
                            'address': screen.address})
        return screens

    def get_groups(self, obj):
        group_screens = GroupScreens.objects.filter(screen=obj)
        groups = []
        for each_group_screen in group_screens:
            group = each_group_screen.group
            groups.append({'group_screen_id': each_group_screen.group_screen_id, 'group_id': group.group_id,
                           'group_name': group.group_name})
        return groups

    def add_content_fields(self, obj, data, fields=None):
        if fields is None:
            fields = self.selected_fields
        for field in fields:
            if field == 'content_id':
                data['content_id'] = obj.content_id
            if field == 'document':
                if obj.is_folder:
                    # TODO: Keep the url as the path to the default folder icon
                    data['url'] = ''
                else:
                    data['url'] = settings.MEDIA_HOST + obj.document.url
            if field == 'title':
                data['title'] = obj.title
            if field == 'is_folder':
                data['is_folder'] = obj.is_folder
        return data

    def get_playlist_items(self, obj, only_files=False):
        playlist_items = PlaylistItems.objects.filter(playlist=obj).order_by('position_index')
        contents = []
        # is_folder is removed as player don't require it. If need be you remove this check and keep the is_folder,
        # as the player will anyway ignore this field
        if only_files:
            content_fields=('title', 'document', 'content_id')
        else:
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
            # This is being used for the functions get_selectable_screens / groups for which we need to set the
            # default value of group_screen_id as -1
            if field == 'group_screen_id':
                data['group_screen_id'] = -1
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
