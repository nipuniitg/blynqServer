from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

from authentication.models import UserDetails, Organization
from customLibrary.views_lib import debugFileLog
from playlistManagement.models import Playlist
from screenManagement.models import Screen, Group, SplitScreen, ScreenPane
from schedule.models import Event


class ScheduleScreens(models.Model):
    # One entry for each screen in a group. ( Obsolete comment? )
    # If only screen is scheduled, then group should be null
    schedule_screen_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='%(class)s_screen_id', blank=True,
                               null=True)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='%(class)s_schedule')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        description = self.schedule.schedule_title if self.schedule and self.schedule.schedule_title else ''
        if self.screen:
            description = description + ' - screen ' + self.screen.screen_name
        if self.group:
            description = description + ' - group ' + self.group.group_name
        return description

    # def delete_event(self):
    #     if self.event:
    #         event = self.event
    #         if event.rule:
    #             rule = event.rule
    #             event.rule = None
    #             event.save()
    #             rule.delete()
    #         self.event = None
    #         self.save()
    #         event.delete()

    # class Meta:
    #     unique_together = (('screen', 'schedule', 'group'))


# @receiver(pre_delete, sender=ScheduleScreens)
# def delete_schedule_screen_event(sender, instance, **kwargs):
#     debugFileLog.info("inside delete_schedule_screen")
#     try:
#         if instance.event:
#             event = instance.event
#             if event.rule:
#                 # rule = event.rule
#                 event.rule = None
#                 event.save()
#                 # multiple events are having the same rule, so not deleting the rule
#                 # rule.delete()
#             instance.event = None
#             instance.save()
#             event.delete()
#     except Exception as e:
#         debugFileLog.exception("Received exception")
#         debugFileLog.exception(e)


class SchedulePlaylists(models.Model):
    schedule_playlist_id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='%(class)s_playlist_id')
    schedule_pane = models.ForeignKey('SchedulePane', on_delete=models.CASCADE, blank=True, null=True)
    position_index = models.IntegerField()

    def __unicode__(self):
        if self.schedule_pane and self.schedule_pane.schedule:
            schedule_title = self.schedule_pane.schedule.schedule_title
        else:
            schedule_title = ''
        playlist_title =  self.playlist.playlist_title if self.playlist and self.playlist.playlist_title else ''
        return schedule_title + '-' + playlist_title


class SchedulePane(models.Model):
    schedule_pane_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='%(class)s_schedule')
    screen_pane = models.ForeignKey(ScreenPane, on_delete=models.PROTECT)
    playlists = models.ManyToManyField(Playlist, through=SchedulePlaylists)
    is_always = models.BooleanField(default=True)
    all_day = models.BooleanField(default=True)
    recurrence_absolute = models.BooleanField(default=False)
    event = models.OneToOneField(Event, on_delete=models.SET_NULL, null=True, related_name='%(class)s_event')

    def __unicode__(self):
        schedule_title = self.schedule.schedule_title if self.schedule.schedule_title else ''
        pane_title = self.screen_pane.pane_title if self.screen_pane.pane_title else ''
        return schedule_title + ' - ' + pane_title


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    schedule_title = models.CharField(max_length=100)
    screens = models.ManyToManyField(Screen, through=ScheduleScreens)
    is_split = models.BooleanField(default=False)
    split_screen = models.ForeignKey(SplitScreen, on_delete=models.PROTECT, null=True)
    schedule_panes = models.ManyToManyField(ScreenPane, through=SchedulePane)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True,
                                        related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    def __unicode__(self):
        return self.schedule_title

    class Meta:
        ordering = ['-last_updated_time']

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Schedule.objects.filter(organization=user_details.organization)
