import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, modify_settings, override_settings
from authentication.models import Role, UserDetails, Organization, City, RequestedQuote
from authentication.views import request_quote
from blynq.settings import STORAGE_LIMIT_PER_ORGANIZATION
from customLibrary.tests_lib import create_role, create_organization, create_userdetails, create_city, create_screen, \
    create_schedule, create_content
from customLibrary.views_lib import string_to_dict, obj_to_json_response, obj_to_json_str


# Create your tests here.


class RoleTest(TestCase):
    def test_role(self):
        role = create_role()
        self.assertTrue(isinstance(role, Role))
        self.assertEqual(role.__unicode__(), role.role_name)
        self.assertEqual(role.natural_key(), role.role_name)


class OrganizationTest(TestCase):
    def test_organization(self):
        organization = create_organization()
        self.assertTrue((isinstance(organization, Organization)))
        self.assertEqual(organization.__unicode__(), organization.organization_name)
        self.assertEqual(organization.natural_key(), organization.organization_name)


class UserDetailsTest(TestCase):
    def test_userdetails(self):
        userdetails = create_userdetails()
        self.assertTrue(isinstance(userdetails, UserDetails))
        self.assertEqual(userdetails.__unicode__(), userdetails.user.username)
        self.assertEqual(userdetails.natural_key(), userdetails.user.username)


class CityTest(TestCase):
    def test_city(self):
        city = create_city()
        self.assertTrue(isinstance(city, City))
        self.assertEqual(city.__unicode__(), city.city_name + ', ' + city.state)
        self.assertEqual(city.natural_key(), {'city_id': city.city_id, 'city_name': city.city_name})


class RequestedQuoteTest(TestCase):
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
    def setUp(self):
        self.factory = RequestFactory()
        user = create_userdetails(default_userdetails=True).user
        assert isinstance(user, User)
        self.user = user

    def test_views_homepage(self):
        user_details = create_userdetails()
        self.client.login(username=user_details.user.username, password='blynq')
        url = reverse("home_page_summary_json")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_data = string_to_dict(response.content)
        self.assertEqual(json_data['schedule_count'], 0)
        self.assertEqual(json_data['used_storage'], 0)
        self.assertEqual(json_data['total_storage'], STORAGE_LIMIT_PER_ORGANIZATION)
        self.assertEqual(json_data['screen_count'], 0)
        screen = create_screen()
        schedule = create_schedule(default_schedule=True)
        content = create_content(default_content=True)
        response = self.client.get(url)
        json_data = string_to_dict(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['screen_count'], 1)
        self.assertEqual(json_data['schedule_count'], 1)
        self.assertEqual(json_data['used_storage'], content.document.size)
        content.delete()
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
