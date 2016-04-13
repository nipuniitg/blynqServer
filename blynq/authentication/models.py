from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

# See https://docs.djangoproject.com/en/1.8/ref/contrib/auth/ for User model details


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name + ', ' + self.state


class Address(models.Model):
    building_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.IntegerField(blank=True)
    added_by = models.ForeignKey('UserDetails', on_delete=models.PROTECT)

    def __unicode__(self):
        return self.building_name + ', ' + self.area + ', ' + self.city.name


'''
One organization should be Blynq
'''


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
    contact = models.CharField(max_length=12, blank=True, null=True)


    def __unicode__(self):
        return self.name


'''
A User can have one of the below roles in increasing hierarchy
viewer - who has only view access to the content and the schedule. Only for monitoring purposes.
scheduler - who can schedule using the existing content but cannot upload new content.
uploader - who can upload new content as well as schedule it.
manager - who can upload+schedule+ modify user roles for that company
'''


class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    role_description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.role_name


class UserDetails(User):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    mobile_number = models.CharField(max_length=12)
    role = models.ForeignKey(Role)

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __unicode__(self):
        return self.username


'''
def Save_User_Details(sender, instance, **kwargs):
    userdetails, new = UserDetails.objects.get_or_create(user = instance)
post_save.connect(Save_User_Details, User)
'''

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
