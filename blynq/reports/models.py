from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.
from customLibrary.views_lib import today_date
from screenManagement.models import Screen


class MediaAnalytics(models.Model):
    player_analytics_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen)
    playlist_id = models.IntegerField(null=True)
    content_id = models.IntegerField(null=True)
    date = models.DateField(default=today_date)
    count = models.IntegerField(default=0)
    time_played = models.IntegerField(default=0) # total_time in seconds this content played

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.screen.screen_name + ' ' + str(self.date) + ' ' + str(self.count)


class ScreenAnalytics(models.Model):
    screen_analytics_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen)
    session_start_time = models.DateTimeField()
    session_end_time = models.DateTimeField()

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.screen.screen_name + 'start ' + self.session_start_time + ' end ' + self.session_end_time
