import os

from django.db import models

from django.utils.translation import ugettext_lazy as _
from authentication.models import UserDetails, Organization
from blynq.settings import MEDIA_ROOT
from customLibrary.custom_settings import PLAYER_UPDATES_DIR, PLAYER_LOG_DIR

# Create your models here.


def upload_to_dir(instance, filename):
    filename = os.path.basename(filename)
    updates_dir = os.path.join(MEDIA_ROOT, PLAYER_UPDATES_DIR)
    if not os.path.exists(updates_dir):
        os.makedirs(updates_dir)
    return '%s/%s' % (PLAYER_UPDATES_DIR, filename)


class PlayerUpdate(models.Model):
    player_update_id = models.AutoField(primary_key=True)
    executable = models.FileField(upload_to=upload_to_dir)
    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_uploaded_by',
                                    null=True)
    comments = models.TextField(blank=True, null=True)
    uploaded_time = models.DateTimeField(_('uploaded time'), auto_now_add=True)
    last_updated_time = models.DateTimeField(_('updated at'), auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_time']

    def __unicode__(self):
        return self.executable.url


class LocalServer(models.Model):
    local_server_id = models.AutoField(primary_key=True)
    local_url = models.CharField(max_length=255)
    # decimal format of the mac-address can be obtained using from uuid import getnode; getnode()
    unique_key = models.CharField(max_length=20,
                                  help_text='Enter the decimal format of MAC-Address of the device as unique key')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.local_url + ' ' + self.organization.name


def upload_to_player_dir(instance, filename):
    filename = os.path.basename(filename)
    return '%s/%s' % (PLAYER_LOG_DIR, filename)


class PlayerLog(models.Model):
    player_log_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=upload_to_player_dir, null=True)
    uploaded_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        player_str = self.file.name if self.file else 'No filename exists'
        return player_str
