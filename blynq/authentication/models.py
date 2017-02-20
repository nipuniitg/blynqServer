from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from blynq.settings import STORAGE_LIMIT_PER_ORGANIZATION

# See https://docs.djangoproject.com/en/1.8/ref/contrib/auth/ for User model details
from customLibrary.views_lib import mail_exception, debugFileLog


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=50)

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.city_name + ', ' + self.state

    def natural_key(self):
        return {'city_id': self.city_id, 'city_name': self.city_name}


# Not being used
# class Address(models.Model):
#     address_id = models.AutoField(primary_key=True)
#     building_name = models.CharField(max_length=100)
#     address_line1 = models.CharField(max_length=100, blank=True)
#     address_line2 = models.CharField(max_length=100, blank=True)
#     area = models.CharField(max_length=100)
#     landmark = models.CharField(max_length=100)
#     city = models.ForeignKey(City, on_delete=models.PROTECT)
#     pincode = models.IntegerField(blank=True)
#     added_by = models.ForeignKey('UserDetails', on_delete=models.SET_NULL, null=True)
#
#     def __unicode__(self):
#         return self.building_name + ', ' + self.area + ', ' + self.city.name
#
#     def natural_key(self):
#         return ((self.building_name, self.area, self.city.name, self.pincode))
#
#     class Meta:
#         unique_together = (('building_name', 'added_by'))


"""
One organization should be Blynq
"""


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=100, db_index=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    # address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=12, blank=True, null=True)
    total_file_size_limit = models.BigIntegerField(default=STORAGE_LIMIT_PER_ORGANIZATION)
    used_file_size = models.BigIntegerField(default=0)
    total_screen_count = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.organization_name

    def natural_key(self):
        return self.organization_name


'''
A User can have one of the below roles in increasing hierarchy
viewer - who has only view access to the content and the schedule. Only for monitoring purposes.
scheduler - who can upload and schedule the content.
manager - who can upload+schedule+ modify user roles for that company
'''


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, null=True)

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.role_name

    def natural_key(self):
        return self.role_name

    @staticmethod
    def default_role():
        try:
            role, created = Role.objects.get_or_create(role_name='manager')
        except Exception as e:
            debugFileLog.error('Unable to get or create manager role')
            mail_exception(str(e))
            role = None
        return role


# class models.User
#     username
#     first_name    optional
#     last_name     optional
#     email         optional
#     password
#     groups
#     user_permissions
#     is_staff
#     is_active
#     is_superuser
#     last_login

mobile_number_regex = RegexValidator(regex=r'^(\+\d{1,3}[- ]?)?\d{10}$',
                                     message="Invalid Mobile Number, make sure mobile number is 10 digits")


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=14, validators=[mobile_number_regex], null=True, blank=True)
    role = models.ForeignKey(Role)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def natural_key(self):
        return self.user.username


class RequestedQuote(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=14, validators=[mobile_number_regex], null=True)
    num_of_devices = models.IntegerField()
    additional_details = models.TextField(blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Quote requested from ' + str(self.email)


# Dummy function to bypass the migration failure. ( AttributeError: 'module' object has no attribute 'upload_to_dir' )
# Remove this function
def upload_to_dir(instance, filename):
    pass
