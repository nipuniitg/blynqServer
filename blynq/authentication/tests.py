import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, modify_settings, override_settings
from authentication.models import Role, UserDetails, Organization, City, RequestedQuote
from authentication.views import request_quote, login, organization_homepage_summary, get_profile_details, \
    update_user_details, change_password
from blynq.settings import STORAGE_LIMIT_PER_ORGANIZATION
from customLibrary.tests_lib import create_role, create_organization, create_userdetails, create_city, create_screen, \
    create_schedule, create_content, verify_posted_dict, verify_get_result
from customLibrary.views_lib import string_to_dict, obj_to_json_response, obj_to_json_str


# Create your tests here.


class RoleTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_role(self):
        role = create_role()
        self.assertTrue(isinstance(role, Role))
        self.assertEqual(role.__unicode__(), role.role_name)
        self.assertEqual(role.natural_key(), role.role_name)


class OrganizationTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_organization(self):
        organization = create_organization()
        self.assertTrue((isinstance(organization, Organization)))
        self.assertEqual(organization.__unicode__(), organization.organization_name)
        self.assertEqual(organization.natural_key(), organization.organization_name)


class UserDetailsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_userdetails(self):
        userdetails = create_userdetails()
        self.assertTrue(isinstance(userdetails, UserDetails))
        self.assertEqual(userdetails.__unicode__(), userdetails.user.username)
        self.assertEqual(userdetails.natural_key(), userdetails.user.username)


class CityTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def test_city(self):
        city = create_city()
        self.assertTrue(isinstance(city, City))
        self.assertEqual(city.__unicode__(), city.city_name + ', ' + city.state)
        self.assertEqual(city.natural_key(), {'city_id': city.city_id, 'city_name': city.city_name})


class RequestedQuoteTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def create_requested_quote(self, name='blynq', email='hello@blynq.in', mobile_number='1234567890',
                               num_of_devices=1):
        return RequestedQuote.objects.get_or_create(name=name, email=email, mobile_number=mobile_number,
                                                    num_of_devices=num_of_devices)[0]

    def test_requested_quote(self):
        quote = self.create_requested_quote()
        self.assertTrue(isinstance(quote, RequestedQuote))
        self.assertEqual(quote.__unicode__(), 'Quote requested from ' + str(quote.email))


# Test views.py
class AuthenticationViewsTest(TestCase):
    fixtures = ['ContentType', 'Role', 'AspectRatio', 'ScreenStatus', 'Layout', 'LayoutPane']

    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user

    # def test_login(self):
    #     user_details = create_userdetails()
    #     url = reverse("auth_login")
    #     trigger_pdb()
    #     self.client.get(reverse("auth_logout"))
    #     posted_data = dict(username=user_details.user.username, password='blynq')
    #     verify_posted_dict(self, posted_data=posted_data, url=url, view_func=login)
    #     self.client.get(reverse("auth_logout"))
    #     posted_data = dict(username=user_details.user.username, password='random')
    #     verify_posted_dict(self, posted_data=posted_data, url=url, view_func=login, success=False)

    def test_views_homepage(self):
        user_details = create_userdetails()
        self.client.login(username=user_details.user.username, password='blynq')
        url = reverse("home_page_summary_json")
        expected_result = dict(schedule_count=0, used_storage=0, total_storage=STORAGE_LIMIT_PER_ORGANIZATION,
                               total_screen_count=0, active_screen_count=0, inactive_screen_count=0)
        verify_get_result(self, expected_result, url, view_func=organization_homepage_summary)
        screen = create_screen()
        schedule = create_schedule(default_schedule=True)
        content = create_content(default_content=True)
        expected_result = dict(schedule_count=1, used_storage=content.document.size,
                               total_storage=STORAGE_LIMIT_PER_ORGANIZATION,
                               total_screen_count=1, active_screen_count=1, inactive_screen_count=0)
        verify_get_result(self, expected_result, url, view_func=organization_homepage_summary)
        # Nothing should change even though we save the content object again
        content.save()
        verify_get_result(self, expected_result, url, view_func=organization_homepage_summary)
        content.delete()
        expected_result['used_storage'] = 0
        verify_get_result(self, expected_result, url, view_func=organization_homepage_summary)
        print 'test_views_homepage completed successfully'

    def test_request_quote(self):
        url = reverse('request_quote')
        posted_data = dict(name='test name 1', email='abcdef@gmail.com', mobile_number='1234567890', num_of_devices=10)
        json_str = obj_to_json_str(posted_data)
        request = self.factory.post(path=url, data=json_str, content_type='application/json')
        # request.user = self.user # to login the user
        response = request_quote(request)
        self.assertEqual(response.status_code, 200)
        response_data = string_to_dict(response.content)
        self.assertTrue(response_data.get('success'))
        self.assertEqual(response_data.get('errors'), [])
        # Verify exception
        posted_data = dict(name='test name 1', email='abcdef@gmail.com', mobile_number='1234567890')
        json_str = obj_to_json_str(posted_data)
        request = self.factory.post(path=url, data=json_str, content_type='application/json')
        response = request_quote(request)
        self.assertEqual(response.status_code, 200)
        response_data = string_to_dict(response.content)
        self.assertFalse(response_data.get('success'))
        print 'test_request_quote completed successfully'

    def test_profile_details(self):
        url = reverse("profile_details")
        user_details = create_userdetails()
        expected_result = dict(first_name=user_details.user.first_name, last_name=user_details.user.last_name,
                               email=user_details.user.email, mobile_number=user_details.mobile_number)
        verify_get_result(self, expected_result=expected_result, url=url, view_func=get_profile_details)

        update_url = reverse("update_user_details")
        posted_data = dict(first_name='first name', last_name='last name',
                           email='abc@gmail.com', mobile_number='0123456789')
        verify_posted_dict(self, posted_data=posted_data, url=update_url, view_func=update_user_details)
        verify_get_result(self, expected_result=posted_data, url=url, view_func=get_profile_details)

    def test_change_password(self):
        user_details = create_userdetails()
        url = reverse("change_password")
        # New password mismatch
        posted_data = dict(current_password='blynq', new_password='new_password', reenter_new_password='new_password1')
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=change_password, success=False)
        self.assertFalse(self.client.login(username=user_details.user.username, password='new_password'))
        # New password match and successful change
        posted_data = dict(current_password='blynq', new_password='new_password', reenter_new_password='new_password')
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=change_password, success=True)
        self.assertTrue(self.client.login(username=user_details.user.username, password='new_password'))
        # Current password mismatch
        posted_data = dict(current_password='blynq', new_password='new_password', reenter_new_password='new_password')
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=change_password, success=False)
        self.assertFalse(self.client.login(username=user_details.user.username, password='blynq'))
        # Change password back to normal
        posted_data = dict(current_password='new_password', new_password='blynq', reenter_new_password='blynq')
        verify_posted_dict(self, posted_data=posted_data, url=url, view_func=change_password, success=True)
        self.assertTrue(self.client.login(username=user_details.user.username, password='blynq'))
