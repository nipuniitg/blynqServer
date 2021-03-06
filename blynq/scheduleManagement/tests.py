import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
# Create your tests here.
from django.utils import timezone

from customLibrary.tests_lib import create_schedule, create_schedule_playlist, create_schedule_screen, create_group, \
    create_userdetails, generate_random_string, verify_posted_dict, \
    generate_schedule_dict, verify_get_result
from customLibrary.views_lib import get_ist_datetime, time_fmt, date_fmt
from playerManagement.views import device_key_active
from scheduleManagement.models import Schedule, SchedulePlaylists, ScheduleScreens
from scheduleManagement.views import get_schedules, get_screen_schedules, \
    get_group_schedules, upsert_schedule, delete_schedule
from screenManagement.models import ScreenActivationKey, GroupScreens


class ScheduleModelsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_schedule(self):
        schedule = create_schedule(default_schedule=True)
        self.assertTrue(isinstance(schedule, Schedule))
        self.assertEqual(schedule.__unicode__(), schedule.schedule_title)

    def test_schedule_playlist(self):
        schedule_playlist = create_schedule_playlist(default_schedule_playlist=True)
        self.assertTrue(isinstance(schedule_playlist, SchedulePlaylists))
        unicode_str = schedule_playlist.schedule_pane.schedule.schedule_title + '-' + schedule_playlist.playlist.playlist_title
        self.assertEqual(schedule_playlist.__unicode__(), unicode_str)

    def test_schedule_screen(self):
        schedule_screen = create_schedule_screen(default_schedule_screen=True)
        self.assertTrue(isinstance(schedule_screen, ScheduleScreens))
        unicode_str = schedule_screen.schedule.schedule_title + ' - screen ' + schedule_screen.screen.screen_name
        self.assertEqual(schedule_screen.__unicode__(), unicode_str )
        group = create_group(default_group=True)
        schedule_screen2 = create_schedule_screen(default_schedule_screen=True, group=group)
        unicode_str = unicode_str + ' - group ' + schedule_screen2.group.group_name
        self.assertTrue(isinstance(schedule_screen2, ScheduleScreens))
        self.assertEqual(schedule_screen2.__unicode__(), unicode_str)


class ScheduleViewsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user

    def test_get_schedules(self):
        url = reverse('get_schedules')
        schedule = create_schedule(default_schedule=True)
        expected_result = [generate_schedule_dict(schedule)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_schedules)
        print 'test_get_schedules completed successfully'

    def test_get_screen_schedules(self):
        schedule_screen = create_schedule_screen(default_schedule_screen=True)
        schedule_screen2 = create_schedule_screen(default_schedule_screen=False)
        screen_id = schedule_screen.screen_id
        url = reverse('get_screen_schedules', kwargs={'screen_id':screen_id})
        expected_result = [generate_schedule_dict(schedule_screen.schedule)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_screen_schedules,
                          screen_id=screen_id)
        screen_id = schedule_screen2.screen_id
        url = reverse('get_screen_schedules', kwargs={'screen_id':screen_id})
        expected_result = [generate_schedule_dict(schedule_screen2.schedule)]
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_screen_schedules,
                          screen_id=screen_id)
        print 'test_get_screen_schedules completed successfully'

    # def test_get_group_schedules(self):
    #     group = create_group(default_group=True)
    #     schedule_group = create_schedule_screen(default_schedule_screen=True, group=group)
    #     schedule_group2 = create_schedule_screen(default_schedule_screen=False, group=group)
    #     schedule_screen = create_schedule_screen(default_schedule_screen=True)
    #     url = reverse('get_group_schedules', kwargs={'group_id': group.group_id})
    #     expected_result = [generate_schedule_dict(schedule_group.schedule),
    #                        generate_schedule_dict(schedule_group2.schedule)]
    #     verify_get_result(self, expected_result=expected_result, url=url, view_func=get_group_schedules,
    #                       group_id=group.group_id)
    #     print 'test_get_group_schedules completed successfully'
    #
#     # def test_get_playlist_schedules(self):
#     #     schedule_playlist = create_schedule_playlist(default_schedule_playlist=True)
#     #     schedule_playlist2 = create_schedule_playlist(default_schedule_playlist=False)
#     #     playlist_id = schedule_playlist.playlist_id
#     #     url = reverse('get_playlist_schedules', kwargs={'playlist_id': playlist_id})
#     #     expected_result = [generate_schedule_dict(schedule_playlist.schedule)]
#     #     verify_get_result(self, expected_result=expected_result, url=url, view_func=get_playlist_schedules,
#     #                       playlist_id=playlist_id)
#     #     print 'test_get_playlist_schedules completed successfully'
#
#     def test_device_key_active(self):
#         url = reverse('device_key_active')
#         device_key = generate_random_string(length=16)
#         try:
#             key = ScreenActivationKey.objects.get(activation_key=device_key)
#             print 'The generated random screen key already exists which is very low probability, re-run the tests again'
#             return
#         except Exception as e:
#             print 'The generated random screen key does not exist, now post it like a new screen'
#         posted_data = dict(device_key=device_key)
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=device_key_active, success=False)
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=device_key_active, success=False)
#         # device_key should be entered into the database after post call
#         key = ScreenActivationKey.objects.get(activation_key=device_key)
#         self.assertTrue(isinstance(key, ScreenActivationKey))
#         self.assertFalse(key.verified)
#         self.assertFalse(key.in_use)
#         key.verified = True
#         key.save()
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=device_key_active, success=True)
#         posted_data = dict(device_key=None)
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=device_key_active, success=False)
#         posted_data = dict(device_key='12345678901234567890')
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=device_key_active, success=False)
#         print 'test_device_key_active completed successfully'
#
#     def verify_schedule_playlists(self, schedule, posted_data):
#         schedule_playlists_ids = SchedulePlaylists.objects.filter(schedule=schedule).values_list('playlist_id', flat=True)
#         schedule_playlists_count = len(schedule_playlists_ids)
#         upserted_playlists = posted_data.get('schedule_playlists')
#         upserted_playlists_count = len(upserted_playlists)
#         self.assertEqual(schedule_playlists_count, upserted_playlists_count)
#
#         upserted_playlists_ids = [playlist_dict['playlist_id'] for playlist_dict in upserted_playlists]
#         self.assertItemsEqual(upserted_playlists_ids,schedule_playlists_ids)
#
#     def verify_timeline(self, event, timeline):
#         if timeline.get('is_always'):
#             self.assertIsNone(event.end_recurring_period)
#         else:
#             start_date = timeline.get('start_date')
#             end_recurring_period = timeline.get('end_recurring_period')
#             event_start = get_ist_datetime(event.start)
#             event_end = get_ist_datetime(event.end)
#             self.assertEqual(start_date, event_start.date().strftime(date_fmt))
#             self.assertEqual(start_date, event_end.date().strftime(date_fmt))
#
#             event_end_recurring_period = get_ist_datetime(event.end_recurring_period)
#             self.assertEqual(end_recurring_period, event_end_recurring_period.date().strftime(date_fmt))
#             if timeline.get('all_day'):
#                 self.assertIsNone(timeline.get('start_time'))
#                 self.assertIsNone(timeline.get('end_time'))
#                 start_time = datetime.time(hour=0, minute=0).strftime(time_fmt)
#                 end_time = datetime.time(hour=23, minute=59).strftime(time_fmt)
#             else:
#                 start_time = timeline.get('start_time')
#                 end_time = timeline.get('end_time')
#             self.assertEqual(start_time, event_start.time().strftime(time_fmt))
#             self.assertEqual(end_time, event_end.time().strftime(time_fmt))
#             self.assertEqual(end_time, event_end_recurring_period.time().strftime(time_fmt))
#
#     def verify_schedule_screens(self, schedule, posted_data):
#         schedule_screens = ScheduleScreens.objects.filter(schedule=schedule, screen__isnull=False,
#                                                              group__isnull=True)
#         schedule_screen_ids = schedule_screens.values_list('screen_id', flat=True)
#         schedule_screens_count = len(schedule_screen_ids)
#         upserted_screens = posted_data['schedule_screens']
#         upserted_screens_count = len(upserted_screens)
#         self.assertEqual(schedule_screens_count, upserted_screens_count)
#         upserted_screen_ids = [screen_dict['screen_id'] for screen_dict in upserted_screens]
#         self.assertItemsEqual(upserted_screen_ids, schedule_screen_ids)
#         for object in schedule_screens:
#             self.assertIsNotNone(object.event)
#             self.verify_timeline(object.event, posted_data.get('timeline'))
#
#     def verify_schedule_groups(self, schedule, posted_data):
#         schedule_groups = ScheduleScreens.objects.filter(schedule=schedule, screen__isnull=True,
#                                                             group__isnull=False)
#         schedule_group_ids = schedule_groups.values_list('group_id', flat=True)
#         schedule_groups_count = len(schedule_group_ids)
#         upserted_groups = posted_data['schedule_groups']
#         upserted_groups_count = len(upserted_groups)
#         self.assertEqual(schedule_groups_count, upserted_groups_count)
#         upserted_group_ids = [group_dict['group_id'] for group_dict in upserted_groups]
#         self.assertItemsEqual(upserted_group_ids, schedule_group_ids)
#         # Now verify that there is one entry for each screen present in the group
#         screen_ids = GroupScreens.objects.filter(group_id__in=schedule_group_ids).values_list('screen_id', flat=True)
#         schedule_screen_ids = ScheduleScreens.objects.filter(
#             schedule=schedule, screen__isnull=False, group_id__in=schedule_group_ids).values_list('screen_id', flat=True)
#         self.assertItemsEqual(screen_ids, schedule_screen_ids)
#         for obj in schedule_groups:
#             self.assertIsNotNone(obj.event)
#             self.verify_timeline(obj.event, posted_data.get('timeline'))
#
#     def verify_schedule_details(self, schedule, posted_data):
#         self.verify_schedule_playlists(schedule=schedule, posted_data=posted_data)
#         self.verify_schedule_screens(schedule=schedule, posted_data=posted_data)
#         self.verify_schedule_groups(schedule=schedule, posted_data=posted_data)
#
#     def test_upsert_schedule(self):
#         url = reverse('upsert_schedule')
#         # generate_schedule_dict will create a schedule, add a screen, a group, a playlist and a timeline
#         posted_data = generate_schedule_dict(schedule=None)
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_schedule)
#         schedule = Schedule.objects.get(schedule_title=posted_data.get('schedule_title'))
#         self.assertTrue(isinstance(schedule, Schedule))
#         self.verify_schedule_details(schedule=schedule, posted_data=posted_data)
#
#         # Modify the added schedule by deleting a group and adding a screen
#         posted_data['schedule_id'] = schedule.schedule_id
#         posted_data['schedule_groups'] = []
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_schedule)
#         self.verify_schedule_details(schedule=schedule, posted_data=posted_data)
#
#         # Change the timeline from is_always to all_day
#         timeline = posted_data['timeline']
#         timeline['is_always'] = False
#         timeline['all_day'] = True
#         timeline['start_date'] = timezone.now().date().strftime(date_fmt)
#         timeline['end_recurring_period'] = (timezone.now() + datetime.timedelta(days=2)).strftime(date_fmt)
#         timeline['interval'] = 1
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_schedule)
#         self.verify_schedule_details(schedule=schedule, posted_data=posted_data)
#         print 'test_upsert_schedule completed successfully'
#
#     def test_delete_schedule(self):
#         url = reverse('delete_schedule')
#         schedule = create_schedule(default_schedule=True)
#         schedule_playlist = create_schedule_playlist(default_schedule_playlist=True)
#         schedule_screen = create_schedule_screen(default_schedule_screen=True)
#         posted_data = dict(schedule_id=schedule.schedule_id)
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=delete_schedule)
#         try:
#             schedule = Schedule.objects.get(schedule_id=schedule.schedule_id)
#             self.assertTrue(False, msg='delete_schedule failed as schedule exists')
#         except Exception as e:
#             try:
#                 schedule_screen = ScheduleScreens.objects.get(schedule_screen_id=schedule_screen.schedule_screen_id)
#                 self.assertTrue(False, msg='delete_schedule failed as schedule screen entry exists')
#             except Exception as e:
#                 try:
#                     schedule_playlist = SchedulePlaylists.objects.get(
#                         schedule_playlist_id=schedule_playlist.schedule_playlist_id)
#                     self.assertTrue(False, msg='delete_schedule failed as schedule screen entry exists')
#                 except Exception as e:
#                     pass
#         # Keep some random schedule_id and check that deletion fails
#         posted_data=dict(schedule_id=12345)
#         verify_posted_dict(self, posted_data=posted_data, url=url, view_func=delete_schedule, success=False)
#         print 'test_delete_schedule completed successfully'
