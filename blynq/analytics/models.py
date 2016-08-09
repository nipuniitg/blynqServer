from django.db import models

# Create your models here.
from customLibrary.views_lib import today_date
from playlistManagement.models import PlaylistItems
from screenManagement.models import Screen


class ContentAnalytics(models.Model):
    playlist_item = models.ForeignKey(PlaylistItems, null=True)
    screen = models.ForeignKey(Screen, null=True)
    date = models.DateField(default=today_date)
    time_played = models.IntegerField(default=0)


class ScreenAnalytics(models.Model):
    screen = models.ForeignKey(Screen, related_name='%(class)s_screen')
    date = models.DateField(default=today_date)
    time_online = models.PositiveIntegerField(default=0)    # in seconds
