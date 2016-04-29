from django.utils.datetime_safe import datetime
from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

from authentication.models import UserDetails
from playlistManagement.models import Playlist
from screenManagement.models import Screen, Group


class ScreenSchedule(models.Model):
    # One entry for each screen in a group.
    # If only screen is scheduled, then group should be null
    screen_schedule_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    schedule_name = models.CharField(max_length=100)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    screens = models.ManyToManyField(Screen, through=ScreenSchedule)

    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)


# This is like the basic Event model.
# I'm planning to use https://github.com/llazzaro/django-scheduler instead
# class Event(models.Model):
#     event_id = models.AutoField(primary_key=True)
#     schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     # If events start_time and end_time is greater than or equal to datetime.now
#     is_valid = models.BooleanField(default=True)
#
#     def update_validity(self):
#         if datetime.now() > self.start_time and datetime.now() > self.end_time:
#             self.is_valid = False
#
#     def is_active(self):
#         if datetime.now() >= self.start_time and datetime.now() < self.end_time:
#             return True
#         return False
