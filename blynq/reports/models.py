from __future__ import unicode_literals

from django.db import models

# Create your models here.
from customLibrary.views_lib import today_date
from screenManagement.models import Screen


class MediaAnalytics(models.Model):
    player_analytics_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen)
    playlist_item_id = models.IntegerField(null=True)
    content_id = models.IntegerField(null=True)
    date = models.DateField(default=today_date)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.screen.screen_name + ' ' + str(self.date) + ' ' + str(self.count)


class ScreenAnalytics(models.Model):
    screen_analytics_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen)
    session_start_time = models.DateTimeField()
    session_end_time = models.DateTimeField()
