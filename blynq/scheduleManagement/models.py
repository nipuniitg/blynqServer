from django.utils.datetime_safe import datetime
from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

from authentication.models import UserDetails, Organization
from playlistManagement.models import Playlist
from screenManagement.models import Screen, Group
from schedule.models import Event


class ScreenSchedule(models.Model):
    # One entry for each screen in a group. ( Obsolete comment? )
    # If only screen is scheduled, then group should be null
    screen_schedule_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='%(class)s_screen_id')
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='%(class)s_schedule')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    # TODO: Remove null=True for event
    # Add one event for each ScreenSchedule since each screen has a different calendar
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True)

    # created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    # created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    # last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True,
    #                                     related_name='%(class)s_last_updated_by')
    # last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    def __unicode__(self):
        return self.schedule.schedule_name + ' - ' + self.screen.screen_name

    # class Meta:
    #     unique_together = (('screen', 'schedule', 'group'))


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    schedule_name = models.CharField(max_length=100)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    screens = models.ManyToManyField(Screen, through=ScreenSchedule)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True,
                                        related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    def __unicode__(self):
        return self.schedule_name

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Schedule.objects.filter(organization=user_details.organization)

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
