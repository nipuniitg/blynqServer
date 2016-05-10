from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

# See https://docs.djangoproject.com/en/1.8/ref/contrib/auth/ for User model details
from blynq.settings import STORAGE_LIMIT_PER_ORGANIZATION


# Not being used
class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name + ', ' + self.state

    def natural_key(self):
        return ((self.name, self.state))


# Not being used
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.IntegerField(blank=True)
    added_by = models.ForeignKey('UserDetails', on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.building_name + ', ' + self.area + ', ' + self.city.name

    def natural_key(self):
        return ((self.building_name, self.area, self.city.name, self.pincode))

    class Meta:
        unique_together = (('building_name', 'added_by'))


'''
One organization should be Blynq
'''


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    website = models.CharField(max_length=100)
    #address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=12, blank=True, null=True)
    total_file_size_limit = models.BigIntegerField(default=STORAGE_LIMIT_PER_ORGANIZATION)
    used_file_size = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.name


'''
A User can have one of the below roles in increasing hierarchy
viewer - who has only view access to the content and the schedule. Only for monitoring purposes.
scheduler - who can upload and schedule the content.
manager - who can upload+schedule+ modify user roles for that company
'''


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    role_description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.role_name

    def natural_key(self):
        return self.role_name


class UserDetails(User):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12)
    role = models.ForeignKey(Role)

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __unicode__(self):
        return self.username

    def natural_key(self):
        return self.username


class RequestedQuote(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    num_of_devices = models.IntegerField()
    additional_details = models.TextField(blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)


# class models.User
#     username
#     first_name
#     last_name
#     email
#     password
#     groups
#     user_permissions
#     is_staff
#     is_active
#     is_superuser
#     last_login
