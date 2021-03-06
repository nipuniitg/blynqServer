from django.db import models
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event

from authentication.models import UserDetails, Organization
from customLibrary.views_lib import debugFileLog, timeit
from layoutManagement.models import LayoutPane, Layout
from playlistManagement.models import Playlist
from screenManagement.models import Screen, Group


# Create your models here.


class ScheduleScreens(models.Model):
    # One entry for each screen in a group. ( Obsolete comment? )
    # If only screen is scheduled, then group should be null
    schedule_screen_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='%(class)s_screen_id', blank=True,
                               null=True)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='%(class)s_schedule')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        description = self.schedule.schedule_title if self.schedule and self.schedule.schedule_title else ''
        if self.screen:
            description = description + ' - screen ' + self.screen.screen_name
        if self.group:
            description = description + ' - group ' + self.group.group_name
        return description


class SchedulePlaylists(models.Model):
    schedule_playlist_id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='%(class)s_playlist_id')
    schedule_pane = models.ForeignKey('SchedulePane', on_delete=models.CASCADE, blank=True, null=True)
    position_index = models.IntegerField()

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)


    def __unicode__(self):
        if self.schedule_pane and self.schedule_pane.schedule:
            schedule_title = self.schedule_pane.schedule.schedule_title
        else:
            schedule_title = ''
        playlist_title = self.playlist.playlist_title if self.playlist and self.playlist.playlist_title else ''
        return schedule_title + '-' + playlist_title


class SchedulePane(models.Model):
    schedule_pane_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='%(class)s_schedule')
    layout_pane = models.ForeignKey(LayoutPane, on_delete=models.PROTECT, null=True, blank=True)
    playlists = models.ManyToManyField(Playlist, through=SchedulePlaylists)
    mute_audio = models.BooleanField(default=False)
    randomize_playlist_items = models.BooleanField(default=False)
    is_always = models.BooleanField(default=True)
    all_day = models.BooleanField(default=True)
    recurrence_absolute = models.BooleanField(default=False)
    event = models.OneToOneField(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_event')

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)


    def __unicode__(self):
        schedule_title = self.schedule.schedule_title if self.schedule.schedule_title else ''
        pane_title = self.layout_pane.title if self.layout_pane.title else ''
        return schedule_title + ' - ' + pane_title

    @property
    def get_schedule_playlists_manager(self):
        return self.scheduleplaylists_set.prefetch_related('playlist')


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    schedule_title = models.CharField(max_length=100)
    schedule_description = models.CharField(max_length=256, null=True, blank=True)
    screens = models.ManyToManyField(Screen, through=ScheduleScreens)
    is_split = models.BooleanField(default=False)
    layout = models.ForeignKey(Layout, on_delete=models.PROTECT, null=True)
    schedule_panes = models.ManyToManyField(LayoutPane, through=SchedulePane)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True, blank=True, null=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True,
                                        related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.schedule_title

    class Meta:
        ordering = ['-last_updated_time']

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Schedule.objects.select_related().prefetch_related('screens', 'schedule_panes').filter(
            organization=user_details.organization)

    @property
    def get_schedule_screens_manager(self):
        """
        :return: RelatedManager object of ScheduleScreens related to this Schedule, queries can be fired using
        self.get_schedule_screens_manager.filter(schedule_screen_id = 1)
        """
        return self.schedulescreens_schedule.select_related()

    @property
    def get_schedule_pane_manager(self):
        """
        :return: RelatedManager object of SchedulePane related to this Schedule, queries can be fired using
        self.get_schedule_pane_manager.filter(schedule_pane_id = 1)
        """
        return self.schedulepane_schedule.select_related().prefetch_related('playlists')

    @timeit
    def update_screens_data(self):
        debugFileLog.info("Inside update_screens_data of schedule %s " % self.schedule_title)
        try:
            schedule_screens = ScheduleScreens.objects.select_related('screen', 'screen__screen_data_modified').filter(
                schedule_id=self.schedule_id)
        except Exception as e:
            debugFileLog.exception('Screens does not exist for the schedule, may be due to pre_save')
            return
        for obj in schedule_screens:
            screen = obj.screen
            if screen:
                screen.data_modified()
            else:
                debugFileLog.error('Got null for screen attribute in schedule %s' % self.schedule_title)

    def get_schedule_screens(self):
        try:
            return self.screens.all().values_list('screen_name', flat=True)
        except:
            pass
        return 'Invalid'
    get_schedule_screens.short_description = 'Screens'
