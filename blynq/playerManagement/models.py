import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from authentication.models import UserDetails, Organization
from blynq.settings import MEDIA_ROOT, MEDIA_HOST
from customLibrary.custom_settings import PLAYER_UPDATES_DIR, PLAYER_LOG_DIR

# Create your models here.
from customLibrary.views_lib import mail_exception, debugFileLog


def get_version_code(full_filename):
    try:
        from externalLibraries.apk_parse.apk import APK
        apkf = APK(full_filename)
        version_code = apkf.get_androidversion_code()
        if version_code:
            return int(version_code)
    except Exception as e:
        mail_exception('Extracting version code for file %s failed with exception %s' % (full_filename, str(e)))
    return None


def upload_to_dir(instance, full_filename):
    filename = os.path.basename(full_filename)
    updates_dir = os.path.join(MEDIA_ROOT, PLAYER_UPDATES_DIR)
    if not os.path.exists(updates_dir):
        os.makedirs(updates_dir)
    return '%s/%s' % (PLAYER_UPDATES_DIR, filename)


class PlayerUpdate(models.Model):
    player_update_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    executable = models.FileField(upload_to=upload_to_dir)
    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_uploaded_by',
                                    null=True)
    comments = models.TextField(blank=True, null=True)
    uploaded_time = models.DateTimeField(_('uploaded time'), auto_now_add=True)
    last_updated_time = models.DateTimeField(_('updated at'), auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['-version', '-uploaded_time']

    def __unicode__(self):
        return self.executable.url

    @property
    def apk_url(self):
        return MEDIA_HOST + self.executable.url

    @property
    def apk_file_path(self):
        return os.path.join(MEDIA_ROOT, self.executable.name)


@receiver(post_save, sender=PlayerUpdate)
def post_save_player_update(sender, instance, **kwargs):
    if not instance.version:
        debugFileLog.info("inside post_save PlayerUpdate")
        version_code = get_version_code(instance.apk_file_path)
        instance.version = version_code
        instance.save()
        debugFileLog.info('Uploaded new APK file with version code %s' % str(version_code))


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
