from random import choice
from string import ascii_uppercase

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from schedule.models import Event, Rule, Calendar
from authentication.models import Role, Organization, UserDetails, City
from blynq.settings import MEDIA_HOST
from contentManagement.models import Content
from customLibrary.views_lib import obj_to_json_str, string_to_dict, get_ist_date_str, get_ist_time_str
from playlistManagement.models import Playlist, PlaylistItems
from scheduleManagement.models import Schedule, SchedulePlaylists, ScheduleScreens
from scheduleManagement.serializers import default_timeline
from screenManagement.models import ScreenStatus, ScreenActivationKey, Group, Screen, GroupScreens


def generate_random_string(length=16):
    return ''.join(choice(ascii_uppercase) for i in range(length))


def create_role(role_name='Manager', description='Manager'):
    return Role.objects.get_or_create(role_name=role_name, description=description)[0]


def create_organization(default_organization=True):
    if default_organization:
        name = 'Blynq'
        website = 'http://www.blynq.in'
    else:
        name = generate_random_string(6)
        website = 'http://www.' + name + '.in'
    return Organization.objects.get_or_create(name=name, defaults={'website':website})[0]


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
    return ScreenStatus.objects.get_or_create(status_name=status_name, description=description)[0]


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
        document = SimpleUploadedFile('test_file.txt', 'these are the file contents!')
    if not userdetails:
        userdetails = create_userdetails()
    try:
        content = Content.objects.get(title=title)
    except Content.DoesNotExist:
        content = Content(title=title, document=document, uploaded_by=userdetails, last_modified_by=userdetails,
                          organization=userdetails.organization, is_folder=is_folder, parent_folder=parent_folder)
        content.save()
    return content


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


def create_schedule(default_schedule=True, userdetails=None):
    if default_schedule:
        schedule_title = 'test schedule 1'
    else:
        schedule_title = generate_random_string(6)
    if not userdetails:
        userdetails = create_userdetails(default_userdetails=True)
    return Schedule.objects.get_or_create(schedule_title=schedule_title,
                                          defaults=dict(created_by=userdetails, last_updated_by=userdetails,
                                                        organization=userdetails.organization))[0]


def create_schedule_playlist(default_schedule_playlist=True, position_index=1):
    playlist = create_playlist(default_playlist=default_schedule_playlist)
    schedule = create_schedule(default_schedule=default_schedule_playlist)
    return SchedulePlaylists.objects.get_or_create(playlist=playlist, schedule=schedule,
                                                   defaults=dict(position_index=position_index))[0]


def create_schedule_screen(default_schedule_screen=True, group=None):
    schedule = create_schedule(default_schedule=default_schedule_screen)
    screen = create_screen(default_screen=default_schedule_screen)
    rule = Rule.objects.create(name=schedule.schedule_title, description=schedule.schedule_title, frequency='DAILY')
    event = Event.objects.create(start=timezone.now(), end=timezone.now(), title=schedule.schedule_title, rule=rule,
                                 calendar=screen.screen_calendar)
    # TODO: Add test cases for event
    return ScheduleScreens.objects.get_or_create(schedule=schedule, screen=screen, group=group, event=event)[0]


def verify_posted_dict(obj, posted_data, url, view_func, success=True, content_type='application/json'):
    if content_type == 'application/json':
        json_str = obj_to_json_str(posted_data)
    else:
        json_str = posted_data
    request = obj.factory.post(url, data=json_str, content_type=content_type)
    request.user = obj.user
    response = view_func(request)
    obj.assertEqual(response.status_code, 200)
    response_data = string_to_dict(response.content)
    try:
        obj.assertEqual(response_data.get('success'), success, msg='Response of the url %s is not valid' % url)
    except AssertionError:
        print 'Received assertion error in the response of success'
        import pdb;pdb.set_trace()


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
        import pdb;pdb.set_trace()
        obj.assertTrue(False, msg='The JSON output of url %s does not match' % url)
    return json_response


def generate_content_dict(content, include_is_folder=True):
    content_dict = {}
    if content:
        content_dict['title'] = content.title
        content_dict['content_id'] = content.content_id
        content_dict['document_type'] = content.document_type
        if include_is_folder:
            content_dict['is_folder'] = content.is_folder
        if content.is_folder:
            content_dict['url'] = ""
        else:
            content_dict['url'] = MEDIA_HOST + content.document.url
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
            del screen_dict['status']
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


def generate_schedule_playlists(schedule=None):
    schedule_playlists_list = []
    if schedule:
        schedule_playlists = SchedulePlaylists.objects.filter(schedule=schedule)
        for schedule_playlist in schedule_playlists:
            playlist_dict = generate_playlist_dict(schedule_playlist.playlist)
            playlist_dict['schedule_playlist_id'] = schedule_playlist.schedule_playlist_id
            schedule_playlists_list.append(playlist_dict)
    else:
        playlist = create_playlist(default_playlist=True)
        schedule_playlists_list.append(dict(schedule_playlist_id=-1, playlist_id=playlist.playlist_id))
    return schedule_playlists_list


def generate_schedule_timeline(schedule=None):
    if not schedule:
        return default_timeline()

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
    schedule_dict = dict()
    if schedule:
        schedule_screens = generate_schedule_screens(schedule)
        schedule_groups = generate_schedule_groups(schedule)
        schedule_playlists = generate_schedule_playlists(schedule)
        timeline = generate_schedule_timeline(schedule)
        schedule_id = schedule.schedule_id
        schedule_title = schedule.schedule_title
        schedule_dict = dict(schedule_id=schedule_id, schedule_title=schedule_title,
                             schedule_playlists=schedule_playlists, schedule_screens=schedule_screens,
                             schedule_groups=schedule_groups, timeline=timeline)
    else:
        schedule_dict['schedule_id'] = -1
        schedule_dict['schedule_title'] = 'test upsert schedule'
        schedule_dict['schedule_playlists'] = generate_schedule_playlists()
        schedule_dict['schedule_screens'] = generate_schedule_screens()
        schedule_dict['schedule_groups'] = generate_schedule_groups()
        schedule_dict['timeline'] = generate_schedule_timeline()
    return schedule_dict