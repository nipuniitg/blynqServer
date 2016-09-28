import mimetypes
import shutil
import urllib
import os

from django.core.exceptions import ValidationError
from django.db import models, NotSupportedError
from django.db.models import Q
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from easy_thumbnails.files import get_thumbnailer

from authentication.models import UserDetails, Organization
from blynq.settings import BASE_DIR, MEDIA_ROOT, USERCONTENT_DIR, DELETED_CONTENT_DIR, DEFAULT_DISPLAY_TIME, MEDIA_HOST
from customLibrary.custom_settings import CONTENT_THUMBNAILS, PERMANENTLY_DELETE_FILES
from customLibrary.views_lib import debugFileLog, get_video_length, full_file_path


class ContentType(models.Model):
    content_type_id = models.AutoField(primary_key=True)
    # file_type is of the format <upload_type>/<file_type>/<extension> like url/image/png, file/image/png,
    # url/web/youtube, url/web/iframe, url/web/other
    # <upload_type> is either file or url.
    file_type = models.CharField(max_length=30)
    supported_encodings = models.TextField(help_text='list of comma separated encodings', null=True, blank=True)

    def __unicode__(self):
        return self.file_type

    def natural_key(self):
        return self.file_type


def upload_to_dir(instance, filename):
    filename = os.path.basename(filename)
    if instance.uploaded_by:
        user_directory = 'user%d' % instance.uploaded_by.id
    else:
        user_directory = 'public'
    return '%s/%s/%s' % (USERCONTENT_DIR, user_directory, filename)


class Content(models.Model):
    # This class includes both files and folders as Content
    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name=_('title'))

    document = models.FileField(upload_to=upload_to_dir, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    widget_text = models.TextField(null=True, blank=True)

    sha1_hash = models.CharField(_('sha1'), max_length=40, blank=True, default='')

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT)

    duration = models.IntegerField(default=DEFAULT_DISPLAY_TIME)

    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_uploaded_by',
                                    null=True)
    uploaded_time = models.DateTimeField(_('uploaded time'), auto_now_add=True)

    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_modified_by',
                                        null=True)
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    # is_inside = null implies the files are in the home directory of the user
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_folder = models.BooleanField(default=False)

    # TODO: call logical_path to update this relative_path when a Content object is created or modified
    relative_path = models.CharField(max_length=1025, default='/')

    def increment_size(self):
        # Now increment the used_file_size of the organization if the file is being saved for the first time
        if self.document and self.pk is None:
            if self.organization.used_file_size + self.document.size <= self.organization.total_file_size_limit:
                self.organization.used_file_size = self.organization.used_file_size + self.document.size
                try:
                    self.organization.save()
                except Exception as e:
                    debugFileLog.exception("Received exception while increasing the organization file usage size")
                    debugFileLog.exception(e)
            else:
                debugFileLog.warning("The organization " + self.organization.organization_name +
                                     " total file size limit exceeded")
                debugFileLog.error("Can't upload file")

    def save(self, *args, **kwargs):
        if self.is_folder:
            super(Content, self).save(*args, **kwargs)
            return
        if self.document:
            url = self.document.url
            full_file_type = 'file/'
        elif self.url:
            url = self.url
            full_file_type = 'url/'
        else:
            url = ''
            full_file_type = ''
        file_type, encoding = mimetypes.guess_type(str(url))
        if file_type:
            full_file_type = full_file_type + file_type
        else:
            full_file_type = None
        try:
            content_type = ContentType.objects.get(file_type=full_file_type)
        except ContentType.DoesNotExist:
            if self.document:
                raise ValidationError(_('Invalid File extension'), code='invalid')
            elif self.widget_text:
                super(Content, self).save(*args, **kwargs)
                return
            debugFileLog.exception("file type does not exist, might be an url")

            def check_youtube_url(url):
                import re
                youtube_url_regex = '^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
                return re.match(youtube_url_regex, url)
            is_youtube = check_youtube_url(url)
            file_type = 'url/web/youtube' if is_youtube else 'url/web/other'
            content_type, created = ContentType.objects.get_or_create(file_type=file_type)
        except ContentType.MultipleObjectsReturned:
            content_type = ContentType.objects.filter(file_type=full_file_type)[0]
        except Exception as e:
            debugFileLog.exception(e)
            raise NotSupportedError('%s is not supported at the moment' % full_file_type)
        self.content_type = content_type
        self.increment_size()
        # Now increment the used_file_size of the organization if the file is being saved for the first time
        if self.document:
            if self.is_video or self.is_audio:
                seconds = get_video_length(full_file_path(self.document.name))
                self.duration = seconds
        super(Content, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def natural_key(self):
        return self.title

    def logical_path(self):
        path = '/'
        instance = self
        while instance.parent_folder:
            path = '/' + instance.parent_folder.title + path
            instance = instance.parent_folder
        return path

    def logical_path_list(self):
        path = []
        instance = self
        current_folder = {'content_id': instance.content_id, 'title': instance.title}
        path.insert(0, current_folder)
        instance = instance.parent_folder
        while instance:
            current_folder = {'content_id': instance.content_id, 'title': instance.title}
            path.insert(0, current_folder)
            instance = instance.parent_folder
        return path

    # class Meta:
    #     ordering = ['-last_modified_time']

    def check_type(self, type_str='image'):
        if not self.document:
            return False
        file_type, encoding = mimetypes.guess_type(str(self.document.url))
        if file_type:
            return type_str in file_type
        else:
            return False

    @property
    def file_path(self):
        if self.document:
            return os.path.join(MEDIA_ROOT, self.document.name)
        return ''

    @property
    def is_image(self):
        return self.check_type(type_str='image')

    @property
    def is_video(self):
        return self.check_type(type_str='video')

    @property
    def is_audio(self):
        return self.check_type(type_str='audio')

    @property
    def is_pdf(self):
        return self.check_type(type_str='application/pdf')

    @property
    def is_widget(self):
        widget = False
        if self.content_type and self.content_type.file_type:
            widget = 'widget' in self.content_type.file_type
        return widget

    def thumbnail_relative_path(self):
        if self.is_folder:
            relative_path = CONTENT_THUMBNAILS['folder']
        elif self.is_audio:
            relative_path = CONTENT_THUMBNAILS['audio']
        elif self.is_video:
            relative_path = CONTENT_THUMBNAILS['video']
        elif self.is_pdf:
            relative_path = CONTENT_THUMBNAILS['pdf']
        elif self.is_image:
            relative_path = get_thumbnailer(self.file_path, str(self.content_id))['avatar'].url
        elif self.is_widget:
            # Right now only rss is supported in widgets. Change this as per type of widgets in the future
            relative_path = CONTENT_THUMBNAILS['rss']
        else:
            relative_path = CONTENT_THUMBNAILS['url']
        return relative_path

    @property
    def thumbnail_url(self):
        relative_path = self.thumbnail_relative_path()
        if self.is_image:
            relative_file_path = relative_path.replace(BASE_DIR, '')
            relative_path = urllib.quote(relative_file_path)
        return MEDIA_HOST + relative_path

    @property
    def thumbnail_path(self):
        return os.path.join(BASE_DIR, self.thumbnail_relative_path())

    def get_url(self):
        if self.document:
            return MEDIA_HOST + self.document.url
        elif self.is_folder:
            return ''
        else:
            return self.url

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Content.objects.filter(organization=user_details.organization)

    @staticmethod
    def get_user_widgets(user_details):
        return Content.objects.filter(Q(organization=user_details.organization) | Q(organization__isnull=True)).filter(
            content_type__file_type__icontains='widget')

    # This includes both files, folders and URLs
    @staticmethod
    def get_user_filesystem(user_details):
        return Content.get_user_relevant_objects(user_details=user_details).exclude(
            content_type__file_type__icontains='widget')


def save_relevant_playlists(content_id):
    debugFileLog.info('save_relevant_playlists')
    try:
        from playlistManagement.models import PlaylistItems
        playlist_items = PlaylistItems.objects.filter(content_id=content_id)
        for item in playlist_items:
            item.playlist.save()
    except Exception as e:
        debugFileLog.exception("Exception while saving the playlist to update last_updated_time")
        debugFileLog.exception(e)


@receiver(post_save, sender=Content)
def post_save_content(sender, instance, **kwargs):
    debugFileLog.info("inside post_save_content")
    save_relevant_playlists(content_id=instance.content_id)


@receiver(pre_delete, sender=Content)
def pre_delete_content(sender, instance, **kwargs):
    debugFileLog.info("inside pre_delete_content")
    if instance.document:
        try:
            organization = instance.organization
            organization.used_file_size = organization.used_file_size - instance.document.size
            if organization.used_file_size < 0:
                organization.used_file_size = 0
            organization.save()
        except Exception as e:
            debugFileLog.exception("Exception while subtracting the deleted file size")
        try:
            src = instance.document.name
            file_src = instance.file_path
            # Delete thumbnail
            if instance.is_image and os.path.exists(instance.thumbnail_path):
                try:
                    os.remove(instance.thumbnail_path)
                except Exception as e:
                    debugFileLog.exception('Deletion of thumbnail %s failed with exception %s' %
                                           (instance.thumbnail_path, str(e)))
            if os.path.exists(file_src):
                if not PERMANENTLY_DELETE_FILES:
                    dst = '%s/organization%d/' % (DELETED_CONTENT_DIR, instance.organization.organization_id)
                    file_dst = os.path.join(MEDIA_ROOT, dst)
                    try:
                        if not os.path.exists(file_dst):
                            os.makedirs(file_dst)
                        full_file_dst = file_dst + os.path.basename(src)
                        shutil.move(file_src, full_file_dst)
                    except Exception as e:
                        debugFileLog.error("Error while moving deleted content to media/deletedcontent/organization_id")
                        debugFileLog.exception(e)
                else:
                    try:
                        os.remove(file_src)
                    except Exception as e:
                        debugFileLog.exception('Permanent deletion of file failed with exception')
                        debugFileLog.exception(e)
            else:
                debugFileLog.error("To be deleted content %s does not exist" % file_src)
        except Exception as e:
            debugFileLog.exception("Unknown exception while deleting content")
            debugFileLog.exception(e)
    save_relevant_playlists(content_id=instance.content_id)


# class Widget(models.Model):
#     widget_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100)
#     # text can be a url or xml or text
#     text = models.TextField()
#     type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT)
#     # organization = null implies it is visible to all the organizations
#     organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
#
#     @staticmethod
#     def get_user_relevant_objects(user_details):
#         return Widget.objects.filter(Q(organization=user_details.organization) | Q(organization__isnull=True))
