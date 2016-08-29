from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# Create your models here.
from authentication.models import UserDetails, Organization
from contentManagement.models import Content
from customLibrary.views_lib import debugFileLog
from screenManagement.models import Screen


class PlaylistItems(models.Model):
    playlist_item_id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    # index signifies the position of content in the playlist
    position_index = models.IntegerField()
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

    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_created_by',
                                   null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL,
                                        related_name='%(class)s_last_updated_by', null=True)
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.playlist_title

    class Meta:
        ordering = ['-last_updated_time']

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Playlist.objects.filter(organization=user_details.organization)


@receiver(pre_delete, sender=Playlist)
@receiver(post_save, sender=Playlist)
def post_save_playlist(sender, instance, **kwargs):
    debugFileLog.info("Inside post_save_playlist")
    from scheduleManagement.models import SchedulePane, ScheduleScreens
    try:
        schedule_ids = SchedulePane.objects.filter(playlists__playlist_id=instance.playlist_id,
                                                   schedule__deleted=False).values_list('schedule_id', flat=True)
        screen_ids = ScheduleScreens.objects.filter(schedule_id__in=schedule_ids).values_list('screen_id', flat=True)
        from playerManagement.views import notify_player
        notify_player(screen_ids=screen_ids)
    except Exception as e:
        debugFileLog.exception("Error while notifying the relevant players related to the playlist %s" %
                               instance.playlist_title)
        debugFileLog.exception(e)
