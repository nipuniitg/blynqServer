from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from authentication.models import Role, UserDetails, Organization, City, RequestedQuote


def create_role(role_name='Manager', description='Manager'):
        return Role.objects.get_or_create(role_name=role_name, description=description)[0]


class RoleTest(TestCase):
    def test_role(self):
        role = create_role()
        self.assertTrue(isinstance(role, Role))
        self.assertEqual(role.__unicode__(), role.role_name)
        self.assertEqual(role.natural_key(), role.role_name)


def create_organization(name='Blynq', website='http://www.blynq.in'):
        return Organization.objects.get_or_create(name=name, website=website)[0]


class OrganizationTest(TestCase):
    def test_organization(self):
        organization = create_organization()
        self.assertTrue((isinstance(organization, Organization)))
        self.assertEqual(organization.__unicode__(), organization.name)
        self.assertEqual(organization.natural_key(), organization.name)


def create_userdetails(username='blynq', organization=None, role=None, password='blynq'):
    user = User.objects.get_or_create(username=username, password=password)[0]
    assert isinstance(user, User)
    if not organization:
        organization = create_organization()
    if not role:
        role = create_role()
    return UserDetails.objects.get_or_create(user=user, organization=organization, role=role,
                                             mobile_number='1234567890')[0]


class UserDetailsTest(TestCase):
    def test_userdetails(self):
        userdetails = create_userdetails()
        self.assertTrue(isinstance(userdetails, UserDetails))
        self.assertEqual(userdetails.__unicode__(), userdetails.user.username)
        self.assertEqual(userdetails.natural_key(), userdetails.user.username)


def create_city(city_name='hyderabad', state='Telangana'):
    return City.objects.get_or_create(city_name=city_name, state=state)[0]


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
# class ViewsTest(TestCase):
#     def test_views_authentication(self):
#         self.client.login(username='blynq', password='blynq')
#         url = reverse("home_page_summary_json")
#         resp = self.client.get(url)
#         self.assertEqual(resp.status_code, 200)