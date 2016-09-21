from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# Create your models here.
from authentication.models import UserDetails, Organization
from blynq.settings import CONTENT_ORGANIZATION_NAME
from contentManagement.models import Content
from customLibrary.views_lib import debugFileLog


class PlaylistItems(models.Model):
    playlist_item_id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    # index signifies the position of content in the playlist
    position_index = models.IntegerField(default=0)
    # display_time is the time for which the content should be displayed
    display_time = models.IntegerField(default=settings.DEFAULT_DISPLAY_TIME)

    def __unicode__(self):
        return self.playlist.playlist_title + ' - ' + self.content.title

    class Meta:
        ordering = ['position_index']

        # def natural_key(self):
        #     return ({'playlist_id': self.playlist.playlist_id, 'content_id': self.content.content_id,
        #              'position_index': self.position_index, 'display_time': self.display_time } )


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    playlist_title = models.CharField(max_length=100)
    playlist_items = models.ManyToManyField(Content, through=PlaylistItems)
    playlist_total_time = models.IntegerField(default=0, blank=True, null=True)

    user_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_created_by',
                                   null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True, blank=True, null=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL,
                                        related_name='%(class)s_last_updated_by', null=True)
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.playlist_title

    class Meta:
        ordering = ['-last_updated_time']

    @staticmethod
    def get_user_visible_objects(user_details):
        return Playlist.objects.filter(organization=user_details.organization, user_visible=True)

    @staticmethod
    def get_user_invisible_playlists(user_details):
        return Playlist.objects.filter(organization=user_details.organization, user_visible=False)

    @staticmethod
    def get_all_playlists(user_details):
        return Playlist.objects.filter(organization=user_details.organization)

    @staticmethod
    def get_blynq_content_playlists():
        return Playlist.objects.filter(organization__organization_name=CONTENT_ORGANIZATION_NAME)


@receiver(post_save, sender=PlaylistItems)
@receiver(post_delete, sender=PlaylistItems)
def playlist_items_changed(sender, instance, **kwargs):
    try:
        playlist_total_time = 0
        total_time = PlaylistItems.objects.filter(playlist_id=instance.playlist_id).aggregate(Sum('display_time'))
        if total_time['display_time__sum']:
            playlist_total_time = total_time['display_time__sum']
        playlist = Playlist.objects.get(playlist_id=instance.playlist_id)
        playlist.playlist_total_time = playlist_total_time
        playlist.save()
        if not playlist.user_visible and playlist.playlist_total_time == 0:
            playlist.delete()
    except Exception as e:
        debugFileLog.exception('Failed to update the playlist total time for playlist_id %d' % instance.playlist_id)
        debugFileLog.exception(e)


@receiver(post_save, sender=Playlist)
@receiver(pre_delete, sender=Playlist)
def post_save_playlist(sender, instance, **kwargs):
    debugFileLog.info("Inside post_save_playlist")
    # Set the last_updated_time for all the schedules having this playlist
    from scheduleManagement.models import SchedulePlaylists
    try:
        schedule_playlists = SchedulePlaylists.objects.filter(playlist_id=instance.playlist_id)
        for each_schedule_playlist in schedule_playlists:
            if each_schedule_playlist.schedule_pane:
                schedule = each_schedule_playlist.schedule_pane.schedule
                if not schedule.deleted:
                    schedule.save()
    except Exception as e:
        debugFileLog.exception("Error while updating the last_updated_time of the schedules "
                               "corresponding to playlist %s" % instance.playlist.playlist_title)
        debugFileLog.exception(e)
