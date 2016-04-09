from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

# Create your models here.
from authentication.models import UserDetails
from contentManagement.models import Content, Folder


class PlaylistItems(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.PROTECT)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT)
    # index signifies the position of content in the playlist
    index = models.IntegerField()
    # display_time is the time for which the content should be displayed
    display_time = models.IntegerField(default=settings.DEFAULT_DISPLAY_TIME)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    playlist_items = models.ManyToManyField(Folder, through=PlaylistItems)

    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True)

