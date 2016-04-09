from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

from authentication.models import UserDetails
from playlistManagement.models import Playlist
from screenManagement.models import Group


class Schedule(models.Model):
    name = models.CharField(max_length=100)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)
    screens = models.ManyToManyField(Group)

    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)


# This is like the basic Event model.
# I'm planning to use https://github.com/llazzaro/django-scheduler instead
class Event(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()