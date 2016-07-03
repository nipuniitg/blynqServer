import os

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
# See https://docs.djangoproject.com/en/1.8/ref/contrib/auth/ for User model details
from blynq.settings import STORAGE_LIMIT_PER_ORGANIZATION, PLAYER_UPDATES_DIR
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=50)

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
    organization_name = models.CharField(max_length=100, unique=True)
    website = models.CharField(max_length=100, null=True)
    # address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=12, blank=True, null=True)
    total_file_size_limit = models.BigIntegerField(default=STORAGE_LIMIT_PER_ORGANIZATION)
    used_file_size = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.organization_name

    def natural_key(self):
        return self.organization_name


class LocalServer(models.Model):
    local_server_id = models.AutoField(primary_key=True)
    local_url = models.CharField(max_length=255)
    # decimal format of the mac-address can be obtained using from uuid import getnode; getnode()
    unique_key = models.CharField(max_length=20,
                                  help_text='Enter the decimal format of MAC-Address of the device as unique key')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.local_url + ' ' + self.organization.name


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

    def __unicode__(self):
        return self.role_name

    def natural_key(self):
        return self.role_name


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return self.user.username

    def natural_key(self):
        return self.user.username


class RequestedQuote(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    num_of_devices = models.IntegerField()
    additional_details = models.TextField(blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Quote requested from ' + str(self.email)


def upload_to_dir(instance, filename):
    filename = os.path.basename(filename)
    title, ext = os.path.splitext(filename)
    try:
        version_num = PlayerUpdate.objects.latest('player_update_id').player_update_id
    except PlayerUpdate.DoesNotExist:
        version_num = 1
    except Exception as e:
        from customLibrary.views_lib import debugFileLog
        debugFileLog.exception(e)
        version_num = 1
    version = '-v' + str(version_num+1)
    title = title + version + ext
    return '%s/%s' % (PLAYER_UPDATES_DIR, title)


class PlayerUpdate(models.Model):
    player_update_id = models.AutoField(primary_key=True)
    executable = models.FileField(upload_to=upload_to_dir)
    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_uploaded_by',
                                    null=True)
    comments = models.TextField(blank=True, null=True)
    uploaded_time = models.DateTimeField(_('uploaded time'), auto_now_add=True)
    last_modified_time = models.DateTimeField(_('modified at'), auto_now=True)

    class Meta:
        ordering = ['-uploaded_time']

    def __unicode__(self):
        return self.executable.url


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
