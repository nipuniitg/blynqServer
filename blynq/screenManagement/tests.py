from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
# Create your tests here.
from customLibrary.tests_lib import create_organization, create_userdetails, create_screen_status, \
    create_screen_activation_key, create_group, create_screen, create_group_screens, generate_random_string, create_city, \
    verify_posted_dict, verify_get_result, generate_screen_dict, generate_group_dict
from screenManagement.models import ScreenStatus, ScreenActivationKey, Group, Screen, GroupScreens
from screenManagement.views import get_screens_json, get_groups_json, upsert_group, delete_group, \
    upsert_screen, get_city_options


class ScreenStatusTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_screen_status_creation(self):
        status = create_screen_status()
        self.assertTrue(isinstance(status, ScreenStatus))
        self.assertEqual(status.__unicode__(), status.status_name)
        self.assertEqual(status.natural_key(), status.status_name)


class ScreenActivationKeyTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_screen_activation_key(self):
        key = create_screen_activation_key()
        self.assertTrue(isinstance(key,ScreenActivationKey))
        self.assertFalse(key.in_use)
        unicode_str = 'serial number {0} key {1}'.format(str(key.device_serial_num), str(key.activation_key))
        self.assertEqual(key.__unicode__(), unicode_str)


class GroupTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_group(self):
        organization1 = create_organization()
        user_details = create_userdetails()
        group1 = create_group(organization=organization1)
        self.assertTrue(isinstance(group1, Group))
        self.assertEqual(group1.__unicode__(), group1.group_name)
        self.assertEqual(group1.natural_key(), {'group_id': group1.group_id, 'group_name': group1.group_name })
        # Verify get_user_relevant_objects
        organization2 = create_organization(default_organization=False)
        group2 = create_group(default_group=False, organization=organization2)
        user_groups = Group.get_user_relevant_objects(user_details=user_details)
        self.assertEqual(list(user_groups), list([group1]))


class ScreenTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_screen(self):
        screen = create_screen()
        self.assertTrue(isinstance(screen, Screen))
        unicode_str = screen.screen_name + ' : ' + screen.owned_by.organization_name
        self.assertEqual(screen.__unicode__(), unicode_str)
        organization2 = create_organization(default_organization=False)
        new_userdetails = create_userdetails(default_userdetails=False, organization=organization2)
        screen2 = create_screen(default_screen=False, userdetails=new_userdetails)
        user_screens = Screen.get_user_relevant_objects(user_details=new_userdetails)
        self.assertEqual(list(user_screens), list([screen2]))


class GroupScreensTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_group_screens(self):
        screen = create_screen()
        group = create_group()
        group_screens = create_group_screens(screen=screen, group=group)
        self.assertTrue(isinstance(group_screens, GroupScreens))
        self.assertEqual(group_screens.__unicode__(),
                         group_screens.screen.screen_name + '-' + group_screens.group.group_name)


class ViewsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user
        self.screen1 = create_screen(default_screen=True)
        self.group1 = create_group(default_group=True)
        self.group_screen = create_group_screens(screen=self.screen1, group=self.group1)
        self.screen2 = create_screen(default_screen=False)
        self.group2 = create_group(default_group=False)

    def test_get_screens_json(self):
        url = reverse('screens_json')
        screens_dicts = [generate_screen_dict(self.screen1), generate_screen_dict(self.screen2)]
        verify_get_result(self, expected_result=screens_dicts, url=url, view_func=get_screens_json)
        print 'test_get_screens_json completed successfully'

    def test_get_groups_json(self):
        url = reverse('groups_json')
        group_dicts = [generate_group_dict(self.group1), generate_group_dict(self.group2)]
        verify_get_result(self, expected_result=group_dicts, url=url, view_func=get_groups_json)
        print 'test_get_groups_json completed successfully'

    def generate_city_dict(self, city):
        return {'city_name': city.city_name, 'city_id': city.city_id}

    def test_get_city_options(self):
        url = reverse('city_options')
        city1 = create_city(default_city=True)
        city2 = create_city(default_city=False)
        city_options = [self.generate_city_dict(city1), self.generate_city_dict(city2)]
        verify_get_result(self, expected_result=city_options, url=url, view_func=get_city_options)
        print 'test_get_city_options completed successfully'

    def test_upsert_group(self):
        url = reverse('upsert_group')
        posted_data = generate_group_dict()
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_group)
        # Now remove screen from the group
        group = Group.objects.get(group_name=posted_data.get('group_name'))
        posted_data['group_id'] = group.group_id
        posted_data['screens'] = []
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=upsert_group)
        self.assertQuerysetEqual(group.groupscreens_set.all(), [], 'Screen is not getting deleted in upsert_group')
        print 'test_upsert_group completed successfully'

    def test_delete_group(self):
        url = reverse('delete_group')
        group = create_group(default_group=False)
        posted_data = {'group_id': group.group_id}
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=delete_group)
        try:
            group = Group.objects.get(group_id = group.group_id)
            self.assertTrue(False, msg='The above query should fail as the group should be deleted')
        except Group.DoesNotExist:
            print 'test_delete_group completed successfully'

    def test_upsert_screen(self):
        url = reverse('upsert_screen')
        screen_dict = generate_screen_dict(self.screen1)
        screen_dict['screen_id'] = -1
        screen_key = create_screen_activation_key()
        screen_dict['activation_key'] = screen_key.activation_key
        for group_screen in screen_dict['groups']:
            group_screen['group_screen_id'] = -1
        verify_posted_dict(self, posted_data=screen_dict, url=url, view_func=upsert_screen)
        # Now remove groups from the above screen_dict and the check upsert_screen
        upserted_screen = Screen.objects.get(unique_device_key=screen_key)
        screen_dict = generate_screen_dict(upserted_screen)
        screen_dict['groups'] = []
        verify_posted_dict(self, posted_data=screen_dict, url=url, view_func=upsert_screen)
        self.assertQuerysetEqual(upserted_screen.groupscreens_set.all(), [],
                                 msg='Groups are not getting deleted properly in the upsert_group view')
        print 'test_upsert_screen completed successfully'

