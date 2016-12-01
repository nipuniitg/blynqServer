from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from authentication.models import UserDetails, Organization
from contentManagement.models import Content
from customLibrary.custom_settings import CONTENT_ORGANIZATION_NAME


# Create your models here.
from customLibrary.views_lib import debugFileLog
from customLibrary.views_lib import mail_exception


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

    USER_CREATED, WIDGET, CONTENT, BLYNQ_TV = 'user_created', 'widget', 'content', 'blynq_tv'
    PLAYLIST_TYPE_CHOICES = (
        (USER_CREATED, 'Playlist created by the User/organization'),
        (WIDGET, 'Playlist automatically created from widget'),
        (CONTENT, 'Playlist automatically created from uploaded content'),
        (BLYNQ_TV, 'Playlist created by the BlynQ organization'),
    )
    playlist_type = models.CharField(max_length=20, choices=PLAYLIST_TYPE_CHOICES, default=PLAYLIST_TYPE_CHOICES[0][0])

    @staticmethod
    def get_user_visible_objects(user_details):
        return Playlist.objects.prefetch_related('playlist_items').filter(organization=user_details.organization, user_visible=True)

    @staticmethod
    def get_user_invisible_playlists(user_details):
        return Playlist.objects.prefetch_related('playlist_items').filter(organization=user_details.organization, user_visible=False)

    @staticmethod
    def get_all_playlists(user_details):
        return Playlist.objects.prefetch_related('playlist_items').filter(organization=user_details.organization)

    @staticmethod
    def get_blynq_content_playlists():
        return Playlist.objects.prefetch_related('playlist_items').filter(organization__organization_name=CONTENT_ORGANIZATION_NAME)

    @staticmethod
    def upsert_playlist(playlist_dict, user_details, user_visible=True):
        playlist_id = int(playlist_dict.get('playlist_id'))
        playlist_title = playlist_dict.get('playlist_title')
        playlist_type = playlist_dict.get('playlist_type')
        playlist_items = playlist_dict.get('playlist_items')
        user_playlists = Playlist.get_user_visible_objects(user_details=user_details)

        # upsert playlist
        if playlist_id == -1:
            playlist = Playlist(playlist_title=playlist_title, created_by=user_details, user_visible=user_visible,
                                playlist_type=playlist_type,
                                last_updated_by=user_details, organization=user_details.organization)
            playlist.save()
            playlist_id = playlist.playlist_id
        else:
            playlist = user_playlists.get(playlist_id=playlist_id)
            playlist.playlist_title = playlist_title
            playlist.last_updated_by = user_details
            playlist.save()

        # upsert playlist items
        playlist_item_id_list = []
        for pos_index, item in enumerate(playlist_items):
            playlist_item_id = int(item.get('playlist_item_id'))
            content_id = int(item.get('content_id'))
            display_time = int(item.get('display_time'))
            content = Content.get_user_relevant_objects(user_details=user_details).get(content_id=content_id)
            if playlist_item_id == -1:
                entry = PlaylistItems.objects.create(playlist=playlist, content=content, position_index=pos_index,
                                                     display_time=display_time)
                playlist_item_id = entry.playlist_item_id
            else:
                entry = playlist.playlistitems_set.get(playlist_item_id=playlist_item_id)
                entry.position_index = pos_index
                entry.display_time = display_time
                entry.save()
            playlist_item_id_list.append(playlist_item_id)

        # Remove content not in playlist_items
        removed_playlist_content = playlist.playlistitems_set.exclude(
            playlist_item_id__in=playlist_item_id_list)
        for content in removed_playlist_content:
            content.delete()
        return playlist
