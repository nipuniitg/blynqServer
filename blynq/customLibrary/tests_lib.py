from random import choice
from string import ascii_uppercase

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from schedule.models import Event, Rule, Calendar
from authentication.models import Role, Organization, UserDetails, City
from blynq.settings import MEDIA_HOST
from contentManagement.models import Content
from customLibrary.views_lib import obj_to_json_str, string_to_dict, get_ist_date_str, get_ist_time_str, \
    datetime_to_string, get_ist_datetime
from layoutManagement.models import Layout, LayoutPane
from playlistManagement.models import Playlist, PlaylistItems
from scheduleManagement.models import Schedule, SchedulePlaylists, ScheduleScreens, SchedulePane
from screenManagement.models import ScreenStatus, ScreenActivationKey, Group, Screen, GroupScreens, AspectRatio


def generate_random_string(length=16):
    return ''.join(choice(ascii_uppercase) for i in range(length))


def trigger_pdb():
    import pdb;pdb.set_trace()


def create_role(role_name='Manager', description='Manager'):
    return Role.objects.get_or_create(role_name=role_name, defaults=dict(description=description))[0]


def create_organization(default_organization=True):
    if default_organization:
        organization_name = 'Blynq'
        website = 'http://www.blynq.in'
    else:
        organization_name = generate_random_string(6)
        website = 'http://www.' + organization_name + '.in'
    return Organization.objects.get_or_create(organization_name=organization_name, defaults={'website':website})[0]


def create_userdetails(default_userdetails=True, organization=None, role=None):
    if default_userdetails:
        username = 'blynq'
        password = 'blynq'
    else:
        username = generate_random_string(6)
        password = username
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password)
    assert isinstance(user, User)
    if not organization:
        organization = create_organization(default_organization=True)
    if not role:
        role = create_role()
    return UserDetails.objects.get_or_create(user=user, organization=organization, role=role,
                                             mobile_number='1234567890')[0]


def create_city(default_city=True):
    if default_city:
        city_name = 'Hyderabad'
        state = 'Telangana'
    else:
        city_name = generate_random_string(6)
        state = city_name
    return City.objects.get_or_create(city_name=city_name, state=state)[0]


def create_screen_status(status_name='Offline', description='The device is not connected to internet'):
    return ScreenStatus.objects.get_or_create(status_name=status_name, defaults=dict(description=description))[0]


def create_screen_activation_key():
    activation_key = generate_random_string(16)
    device_serial_num = activation_key
    return ScreenActivationKey.objects.get_or_create(activation_key=activation_key,
                                                     device_serial_num=device_serial_num,
                                                     verified=True)[0]


def create_group(default_group=True, organization=None):
    if default_group:
        group_name = 'Test name'
        description = 'test description'
    else:
        group_name = generate_random_string(6)
        description = group_name
    if not organization:
        organization=create_organization(default_organization=True)
    return Group.objects.get_or_create(group_name=group_name, description=description, organization=organization,
                                       created_on=timezone.now())[0]


def create_screen(default_screen=True, userdetails=None):
    if default_screen:
        screen_name = 'test screen 1'
        address = 'test address'
    else:
        screen_name = generate_random_string(6)
        address = screen_name
    city = create_city()
    screen_key = create_screen_activation_key()
    screen_key.in_use=True
    screen_key.save()
    if not userdetails:
        userdetails = create_userdetails()
    unique_str = generate_random_string(5)
    calendar = Calendar.objects.create(name=unique_str, slug=unique_str)
    screen_status = create_screen_status()
    return Screen.objects.get_or_create(screen_name=screen_name, defaults=dict(address=address, city=city,
                                                                               unique_device_key=screen_key,
                                                                               activated_by=userdetails,
                                                                               status=screen_status,
                                                                               owned_by=userdetails.organization,
                                                                               screen_calendar=calendar))[0]


def create_group_screens(screen, group):
    return GroupScreens.objects.get_or_create(screen=screen, group=group)[0]


def create_content(default_content=True, is_folder=False, userdetails=None, parent_folder=None):
    if default_content:
        if is_folder:
            title = 'test folder 1'
        else:
            title = 'test content 1'
    else:
        title = generate_random_string(6)
    print 'content title is ', title
    if is_folder:
        document = None
    else:
        document = SimpleUploadedFile('test_file.jpg', 'these are the file contents!')
    if not userdetails:
        userdetails = create_userdetails()
    try:
        content = Content.objects.get(title=title)
    except Content.DoesNotExist:
        content = Content(title=title, document=document, uploaded_by=userdetails, last_updated_by=userdetails,
                          organization=userdetails.organization, is_folder=is_folder, parent_folder=parent_folder)
        content.save()
    return content


def default_aspect_ratio():
    return AspectRatio.objects.get(aspect_ratio_id=1)


def full_screen_layout():
    try:
        return Layout.objects.get(layout_id=1)
    except Exception as e:
        print 'Default Full Screen Layout does not exist'
        trigger_pdb()


def create_layout(default_layout=True, is_split=False, userdetails=None):
    if not is_split:
        return full_screen_layout()
    elif default_layout:
        layout_title = 'test layout 1'
    else:
        layout_title = generate_random_string(6)
    if not userdetails:
        userdetails = create_userdetails(default_userdetails=True)
    try:
        return Layout.objects.get_or_create(title=layout_title, defaults=dict(
            aspect_ratio=default_aspect_ratio(), created_by=userdetails, last_updated_by=userdetails,
            organization=userdetails.organization, is_default=False))[0]    # return layout in layout, created
    except Exception as e:
        print 'Error in layout creation'
        trigger_pdb()


def create_layout_pane(default_layout_pane=True, left_margin=0, top_margin=0, z_index=0, width=50, height=50,
                       layout=None):
    if default_layout_pane:
        layout_pane_title = 'test pane 1'
    else:
        layout_pane_title = generate_random_string(6)
    if not layout:
        layout = create_layout(default_layout=True)
    return LayoutPane.objects.get_or_create(title=layout_pane_title, defaults=dict(
        left_margin=left_margin, top_margin=top_margin, z_index=z_index, width=width, height=height, layout=layout))[0]


def create_playlist(default_playlist=True, userdetails=None):
    if default_playlist:
        playlist_title = 'test playlist 1'
    else:
        playlist_title = generate_random_string(6)
    if not userdetails:
        userdetails = create_userdetails(default_userdetails=True)
    return Playlist.objects.get_or_create(playlist_title=playlist_title,
                                          defaults=dict(created_by=userdetails, last_updated_by=userdetails,
                                                        organization=userdetails.organization))[0]


def create_playlist_items(default_playlist_item=True, position_index=1, display_time=15, playlist=None):
    # Increment position_index for each playlist item in a playlist
    content = create_content(default_content=default_playlist_item)
    if not playlist:
        playlist = create_playlist(default_playlist=default_playlist_item)
    return PlaylistItems.objects.get_or_create(playlist=playlist, content=content,
                                               defaults=dict(position_index=position_index, display_time=display_time))[0]


def create_schedule(default_schedule=True, is_split=False, userdetails=None):
    if default_schedule:
        schedule_title = 'test schedule 1'
    else:
        schedule_title = generate_random_string(6)
    if not userdetails:
        userdetails = create_userdetails(default_userdetails=True)
    layout = create_layout(default_layout=default_schedule, is_split=is_split, userdetails=userdetails)
    return Schedule.objects.get_or_create(schedule_title=schedule_title, is_split=is_split, layout=layout,
                                          defaults=dict(created_by=userdetails, last_updated_by=userdetails,
                                                        organization=userdetails.organization))[0]


def create_schedule_playlist(default_schedule_playlist=True, is_split=False, userdetails=None, position_index=1):
    playlist = create_playlist(default_playlist=default_schedule_playlist)
    schedule_pane = create_schedule_pane(default_schedule_pane=default_schedule_playlist, is_split=is_split,
                                         userdetails=userdetails)
    return SchedulePlaylists.objects.get_or_create(playlist=playlist, schedule_pane=schedule_pane,
                                                   defaults=dict(position_index=position_index))[0]


def create_schedule_pane(default_schedule_pane=True, is_split=False, userdetails=None):
    schedule = create_schedule(default_schedule=default_schedule_pane)
    layout = create_layout(default_layout=default_schedule_pane, is_split=is_split, userdetails=userdetails)
    layout_pane = create_layout_pane(default_layout_pane=default_schedule_pane, layout=layout)
    rule = Rule.objects.create(name=schedule.schedule_title, description=schedule.schedule_title, frequency='DAILY')
    event = Event.objects.create(start=timezone.now(), end=timezone.now(), title=schedule.schedule_title, rule=rule)
    try:
        return SchedulePane.objects.get_or_create(schedule=schedule, layout_pane=layout_pane, event=event)[0]
    except Exception as e:
        trigger_pdb()


def create_schedule_screen(default_schedule_screen=True, group=None):
    schedule = create_schedule(default_schedule=default_schedule_screen)
    screen = create_screen(default_screen=default_schedule_screen)
    return ScheduleScreens.objects.get_or_create(schedule=schedule, screen=screen, group=group)[0]


def verify_posted_dict(obj, posted_data, url, view_func, success=True, content_type='application/json', redirect=False):
    if content_type == 'application/json':
        json_str = obj_to_json_str(posted_data)
    else:
        json_str = posted_data
    request = obj.factory.post(url, data=json_str, content_type=content_type)
    request.user = obj.user
    response = view_func(request)
    if redirect:
        obj.assertEqual(response.status_code, 302)
        return
    obj.assertEqual(response.status_code, 200)
    response_data = string_to_dict(response.content)
    try:
        obj.assertEqual(response_data.get('success'), success, msg='Response of the url %s is not valid' % url)
    except AssertionError:
        print 'Received assertion error in the response of success'
        trigger_pdb()
        obj.assertTrue(False, msg='Success in response of url %s does not match' % url)


def verify_get_result(obj, expected_result, url, view_func, *args, **kwargs):
    request = obj.factory.get(url)
    # login the user
    request.user = obj.user
    response = view_func(request, *args, **kwargs)
    obj.assertEqual(response.status_code, 200)
    json_response = string_to_dict(response.content)
    try:
        obj.assertItemsEqual(expected_result, json_response)
    except AssertionError:
        print "Expected result does not match the response"
        print "Expected result:"
        print expected_result
        print "Received response:"
        print json_response
        trigger_pdb()
        obj.assertTrue(False, msg='The JSON output of url %s does not match' % url)
    return json_response


def generate_content_dict(content, include_is_folder=True):
    content_dict = {}
    if content:
        content_dict['title'] = content.title
        content_dict['content_id'] = content.content_id
        content_dict['content_type'] = content.content_type.file_type if content.content_type else None
        if include_is_folder:
            content_dict['is_folder'] = content.is_folder
        if content.document:
            content_dict['url'] = MEDIA_HOST + content.document.url
        elif content.is_folder or content.is_text_scroll_widget:
            content_dict['url'] = ''
        else:
            content_dict['url'] = content.url
        content_dict['thumbnail'] = content.thumbnail_url
        content_dict['duration'] = content.duration
        if content.is_text_scroll_widget:
            content_dict['widget_text'] = content.widget_text
    return content_dict


def generate_screen_dict(screen):
    screen_dict = {}
    if not screen:
        return screen_dict
    screen_dict['status'] = screen.status.status_name if screen.status else None
    screen_dict['city'] = {'city_id': screen.city.city_id, 'city_name': screen.city.city_name} if screen.city else None
    screen_dict['screen_name'] = screen.screen_name
    screen_dict['screen_size'] = screen.screen_size
    screen_dict['address'] = screen.address
    screen_dict['resolution'] = screen.resolution
    screen_dict['screen_id'] = screen.screen_id
    screen_dict['status'] = screen.current_status
    screen_dict['last_active_time'] = datetime_to_string(get_ist_datetime(screen.last_active_time))
    screen_dict['aspect_ratio'] = screen.aspect_ratio
    group_dicts = []
    for group_screen in screen.groupscreens_set.all():
        group_dicts.append({'group_id': group_screen.group.group_id, 'group_name': group_screen.group.group_name,
                            'group_screen_id': group_screen.group_screen_id})
    screen_dict['groups'] = group_dicts
    return screen_dict


def generate_playlist_item_dict(playlist_item=None, content=None):
    playlist_item_dict = {}
    if playlist_item:
        playlist_item_dict = generate_content_dict(playlist_item.content)
        playlist_item_dict['playlist_item_id'] = playlist_item.playlist_item_id
        playlist_item_dict['display_time'] = playlist_item.display_time
    else:
        playlist_item_dict['playlist_item_id'] = -1
        playlist_item_dict['display_time'] = 15
        playlist_item_dict['content_id'] = content.content_id
    return playlist_item_dict


def generate_playlist_dict(playlist):
    playlist_dict = {}
    if playlist:
        playlist_dict = dict(playlist_id=playlist.playlist_id, playlist_title=playlist.playlist_title)
        playlist_items = []
        for playlist_item in playlist.playlistitems_set.all():
            playlist_items.append(generate_playlist_item_dict(playlist_item))
        playlist_dict['playlist_items'] = playlist_items
    return playlist_dict


def generate_group_dict(group=None):
    group_dict = {}
    if group:
        group_dict['group_id'] = group.group_id
        group_dict['description'] = group.description
        group_dict['group_name'] = group.group_name
        screen_dicts = []
        for group_screen in group.groupscreens_set.all():
            screen_dict = generate_screen_dict(group_screen.screen)
            del screen_dict['groups']
            # Fix this difference of not showing aspect_ratio in the screen_dict
            screen_dict['aspect_ratio'] = group_screen.screen.aspect_ratio
            screen_dict['group_screen_id'] = group_screen.group_screen_id
            screen_dicts.append(screen_dict)
        group_dict['screens'] = screen_dicts
    else:
        group_dict['group_id'] = -1
        group_dict['group_name'] = 'create group 1'
        group_dict['description'] = 'create group description'
        screen = create_screen(default_screen=True)
        group_dict['screens'] = [{'group_screen_id': -1, 'screen_id': screen.screen_id}]
    return group_dict


def generate_aspect_ratio_dict(aspect_ratio):
    return dict(aspect_ratio_id=aspect_ratio.aspect_ratio_id, title=aspect_ratio.title,
                orientation=aspect_ratio.orientation, width_component=aspect_ratio.width_component,
                height_component=aspect_ratio.height_component)


def generate_layout_pane_dict(pane=None):
    if pane:
        layout_pane_dict = dict(layout_pane_id=pane.layout_pane_id, title=pane.title, left_margin=pane.left_margin,
                                top_margin=pane.top_margin, z_index=pane.z_index, width=pane.width, height=pane.height)
    else:
        layout_pane_dict = dict(layout_pane_id=-1, title=generate_random_string(6), left_margin=0, top_margin=0, z_index=0,
                                width=50, height=50)
    return layout_pane_dict


def generate_layout_dict(layout=None):
    if layout:
        layout_panes = LayoutPane.objects.filter(layout=layout)
        layout_panes_list = []
        for pane in layout_panes:
            layout_panes_list.append(generate_layout_pane_dict(pane))
        layout_dict = dict(layout_id=layout.layout_id, title=layout.title, layout_panes=layout_panes_list,
                           aspect_ratio=generate_aspect_ratio_dict(layout.aspect_ratio))
    else:
        layout_dict = dict(layout_id=-1, title=generate_random_string(6), layout_panes=[generate_layout_pane_dict()],
                           aspect_ratio=generate_aspect_ratio_dict(default_aspect_ratio()))
    return layout_dict


def default_timeline(is_always=True, all_day=True, recurrence_absolute=False, start_date=None, end_recurring_period=None,
                     start_time=None, end_time=None, frequency=None, interval=None, byweekday=None, bymonthday=None,
                     byweekno=None):
    return {'is_always': is_always, 'recurrence_absolute': recurrence_absolute, 'all_day': all_day,
            'start_date':start_date, 'end_recurring_period': end_recurring_period, 'start_time': start_time,
            'end_time': end_time, 'frequency':frequency, 'interval': interval, 'byweekday': byweekday,
            'bymonthday': bymonthday, 'byweekno': byweekno }


def generate_schedule_screens(schedule=None):
    schedule_screens_list = []
    if schedule:
        schedule_screens = ScheduleScreens.objects.filter(schedule=schedule, screen__isnull=False, group__isnull=True)
        for schedule_screen in schedule_screens:
            screen_dict = generate_screen_dict(schedule_screen.screen)
            screen_dict['schedule_screen_id'] = schedule_screen.schedule_screen_id
            schedule_screens_list.append(screen_dict)
    else:
        screen = create_screen(default_screen=True)
        schedule_screens_list.append(dict(schedule_screen_id=-1, screen_id=screen.screen_id))
    return schedule_screens_list


def generate_schedule_groups(schedule=None):
    schedule_groups_list = []
    if schedule:
        schedule_groups = ScheduleScreens.objects.filter(schedule=schedule, screen__isnull=True, group__isnull=False)
        for schedule_group in schedule_groups:
            group_dict = generate_group_dict(schedule_group.group)
            group_dict['schedule_screen_id'] = schedule_group.schedule_screen_id
            schedule_groups_list.append(group_dict)
    else:
        group = create_group(default_group=True)
        schedule_groups_list.append(dict(schedule_screen_id=-1, group_id=group.group_id))
    return schedule_groups_list


def generate_schedule_playlists(schedule_pane=None):
    schedule_playlists_list = []
    if schedule_pane:
        schedule_playlists = SchedulePlaylists.objects.filter(schedule=schedule_pane)
        for schedule_playlist in schedule_playlists:
            playlist_dict = generate_playlist_dict(schedule_playlist.playlist)
            playlist_dict['schedule_playlist_id'] = schedule_playlist.schedule_playlist_id
            schedule_playlists_list.append(playlist_dict)
    else:
        playlist = create_playlist(default_playlist=True)
        schedule_playlists_list.append(dict(schedule_playlist_id=-1, playlist_id=playlist.playlist_id))
    return schedule_playlists_list


def generate_schedule_panes(schedule=None):
    schedule_panes_list = []
    if schedule:
        schedule_panes = SchedulePane.objects.filter(schedule=schedule)
    else:
        schedule_panes = full_screen_layout().layoutpane_layout.all()
    for schedule_pane in schedule_panes:
        schedule_blynq_playlists = []
        schedule_widgets = []
        mute_audio = schedule_pane.mute_audio
        schedule_playlists = generate_schedule_playlists(schedule_pane)
        layout_pane = generate_layout_pane_dict(schedule_pane.layout_pane)
        timeline = generate_schedule_timeline(schedule)
        schedule_pane_id = schedule_pane.schedule_pane_id
        schedule_pane_dict = dict(schedule_pane_id=schedule_pane_id, schedule_blynq_playlists=schedule_blynq_playlists,
                                  schedule_widgets=schedule_widgets, mute_audio=mute_audio,
                                  schedule_playlists=schedule_playlists, layout_pane=layout_pane, timeline=timeline)
        schedule_panes_list.append(schedule_pane_dict)
    return schedule_panes_list


def generate_schedule_timeline(schedule=None, is_always=True, all_day=True, recurrence_absolute=False):
    if not schedule:
        return default_timeline(is_always=is_always, all_day=all_day, recurrence_absolute=recurrence_absolute)
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


def generate_schedule_dict(schedule=None):
    if schedule:
        schedule_screens = generate_schedule_screens(schedule)
        schedule_groups = generate_schedule_groups(schedule)
        layout = generate_layout_dict(schedule.layout)
        schedule_panes = generate_schedule_panes(schedule)
        schedule_id = schedule.schedule_id
        schedule_title = schedule.schedule_title
        is_split = schedule.is_split
        schedule_dict = dict(schedule_id=schedule_id, schedule_title=schedule_title, layout=layout, is_split=is_split,
                             schedule_screens=schedule_screens, schedule_groups=schedule_groups,
                             schedule_panes=schedule_panes)
    else:
        layout = generate_layout_dict(full_screen_layout())
        schedule_dict = dict(schedule_id=-1, schedule_title='test upsert schedule', layout=layout, is_split=False,
                             schedule_screens=generate_schedule_screens(), schedule_groups=generate_schedule_groups(),
                             schedule_panes=generate_schedule_panes())
    return schedule_dict
