from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from authentication.models import UserDetails, Organization
from contentManagement.models import Content
from customLibrary.custom_settings import CONTENT_ORGANIZATION_NAME


# Create your models here.


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
