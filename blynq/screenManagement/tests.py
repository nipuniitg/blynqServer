from django.test import TestCase

# Create your tests here.
from django.utils import timezone

from authentication.tests import create_city, create_organization, create_userdetails
from screenManagement.models import ScreenStatus, ScreenActivationKey, Group, Screen, GroupScreens


def create_screen_status(status_name='Online', description='The device is connected to internet'):
    return ScreenStatus.objects.get_or_create(status_name=status_name, description=description)[0]


class ScreenStatusTest(TestCase):
    def test_screen_status_creation(self):
        status = create_screen_status()
        self.assertTrue(isinstance(status, ScreenStatus))
        self.assertEqual(status.__unicode__(), status.status_name)
        self.assertEqual(status.natural_key(), status.status_name)


def create_screen_activation_key(activation_key='1111000011110000', device_serial_num='abcdefghijklmopqrstu'):
    return ScreenActivationKey.objects.get_or_create(activation_key=activation_key,
                                                     device_serial_num=device_serial_num)[0]


class ScreenActivationKeyTest(TestCase):
    def test_screen_activation_key(self):
        key = create_screen_activation_key()
        self.assertTrue(isinstance(key,ScreenActivationKey))
        self.assertFalse(key.verified)
        self.assertFalse(key.in_use)
        unicode_str = 'serial number {0} key {1}'.format(str(key.device_serial_num), str(key.activation_key))
        self.assertEqual(key.__unicode__(), unicode_str)


def create_group(group_name='Test name', description='test description', organization=None):
    return Group.objects.get_or_create(group_name=group_name, description=description, organization=organization,
                                       created_on=timezone.now())[0]


class GroupTest(TestCase):
    def test_group(self):
        organization1 = create_organization()
        user_details = create_userdetails()
        group1 = create_group(organization=organization1)
        self.assertTrue(isinstance(group1, Group))
        self.assertEqual(group1.__unicode__(), group1.group_name)
        self.assertEqual(group1.natural_key(), {'group_id': group1.group_id, 'group_name': group1.group_name })
        # Verify get_user_relevant_objects
        organization2 = create_organization(name='Test organization 2', website='http://www.testorg.in')
        group2 = create_group(group_name='test 2', description='desc 2', organization=organization2)
        user_groups = Group.get_user_relevant_objects(user_details=user_details)
        self.assertEqual(list(user_groups), list([group1]))


def create_screen(screen_name='test 1', address='', organization=None, screen_key=None):
    city = create_city()
    if not screen_key:
        screen_key = create_screen_activation_key()
    screen_key.in_use=True
    screen_key.verified=True
    screen_key.save()
    if not organization:
        organization = create_organization()
    return Screen.objects.get_or_create(screen_name=screen_name, address=address, city=city,
                                        unique_device_key=screen_key, owned_by=organization)[0]


class ScreenTest(TestCase):
    def test_screen(self):
        screen = create_screen()
        user_details = create_userdetails()
        self.assertTrue(isinstance(screen, Screen))
        self.assertEqual(screen.__unicode__(), screen.screen_name)
        organization2 = create_organization('test organization 2', 'http://www.testorg2.in')
        screen_key = create_screen_activation_key('0123456789012345', 'qwwertyuiop')
        self.assertTrue(isinstance(screen_key, ScreenActivationKey))
        screen2 = create_screen(screen_name='test 2', address='', organization=organization2, screen_key=screen_key)
        user_screens = Screen.get_user_relevant_objects(user_details=user_details)
        self.assertEqual(list(user_screens), list([screen]))


def create_group_screens(screen, group):
    return GroupScreens.objects.get_or_create(screen=screen, group=group)[0]


class GroupScreensTest(TestCase):
    def test_group_screens(self):
        screen = create_screen()
        group = create_group()
        group_screens = create_group_screens(screen=screen, group=group)
        self.assertTrue(isinstance(group_screens, GroupScreens))
        self.assertEqual(group_screens.__unicode__(),
                         group_screens.screen.screen_name + '-' + group_screens.group.group_name)