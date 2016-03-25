from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

# See https://docs.djangoproject.com/en/1.8/ref/contrib/auth/ for User model details


'''
First organization should be Blynq, which we assign to UserDetails by default.
'''


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
    mobile_number = models.IntegerField()
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return self.User.username


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
