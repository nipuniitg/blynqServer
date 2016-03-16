from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


class UserDetails(models.Model):
    user = models.OneToOneField(User)
    companyName = models.CharField(max_length=100)
    mobileNumber = models.IntegerField()

    def __unicode__(self):
        return self.User.username

'''
def Save_User_Details(sender, instance, **kwargs):
    userdetails, new = UserDetails.objects.get_or_create(user = instance)
post_save.connect(Save_User_Details, User)
'''
