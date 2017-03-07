import mimetypes
import os, re

from django.core.exceptions import ValidationError
from django.db import models, NotSupportedError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from easy_thumbnails.files import get_thumbnailer

from authentication.models import UserDetails, Organization
from blynq.settings import BASE_DIR, MEDIA_ROOT, USERCONTENT_DIR, DEFAULT_DISPLAY_TIME, MEDIA_HOST
from customLibrary.custom_settings import CONTENT_THUMBNAILS, CONTENT_ORGANIZATION_NAME
from customLibrary.views_lib import debugFileLog, get_video_length, full_file_path, mail_exception


def is_youtube_url(url):
    youtube_url_regex = '^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
    return re.match(youtube_url_regex, url)


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
                    mail_exception(exception=e)
            else:
                debugFileLog.warning("The organization " + self.organization.organization_name +
                                     " total file size limit exceeded")
                debugFileLog.error("Can't upload file")

    def decrement_size(self):
        if self.document:
            try:
                organization = self.organization
                organization.used_file_size = organization.used_file_size - self.document.size
                if organization.used_file_size < 0:
                    organization.used_file_size = 0
                organization.save()
            except Exception as e:
                debugFileLog.exception("Exception while subtracting the deleted file size")

    def handle_content_type(self):
        if self.content_type and not self.url:
            return
        # User might only change web url to youtube or wise versa
        # content_type for other Content objects will remain the same
        if self.url:
            url = str(self.url)
        elif self.document:
            url = str(self.document.url)
        elif not self.content_type:
            mail_exception('Error content_type not set for widget %s' % str(self.content_id),
                           subject='Error in handle_content_type')
            return
        else:
            return
        file_type, encoding = mimetypes.guess_type(url)
        if file_type:
            # Videos or images hosted on other servers should also be treated as files
            full_file_type = 'file/' + file_type
        elif is_youtube_url(url):
            full_file_type = 'url/web/youtube'
        else:
            full_file_type = 'url/web/other'
        try:
            content_type = ContentType.objects.get(file_type=full_file_type)
            self.content_type = content_type
        except ContentType.DoesNotExist:
            error = '%s is not supported at the moment' % url
            mail_exception(error)
            raise NotSupportedError(error)
        except ContentType.MultipleObjectsReturned:
            self.content_type = ContentType.objects.filter(file_type=full_file_type)[0]
        except Exception as e:
            error = '%s is not supported at the moment' % url
            mail_exception(error)
            raise NotSupportedError(error)

    def save(self, *args, **kwargs):
        self.handle_content_type()
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

    @property
    def is_text_scroll_widget(self):
        widget = False
        if self.content_type and self.content_type.file_type:
            widget = 'widget/rss/text' in self.content_type.file_type
        return widget

    @property
    def is_fb_widget(self):
        fb_widget = False
        if self.content_type and self.content_type.file_type:
            fb_widget = 'widget/fb/page' in self.content_type.file_type
        return fb_widget

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
            try:
                full_path = get_thumbnailer(self.file_path, str(self.content_id))['avatar'].url
                relative_path = full_path.replace(BASE_DIR, '')
            except Exception as e:
                debugFileLog.exception(e)
                # TODO: Add an image icon or Not found icon if the image is missing
                relative_path = CONTENT_THUMBNAILS['url']
        elif self.is_fb_widget:
            relative_path = CONTENT_THUMBNAILS['fb']
        elif self.is_text_scroll_widget:
            # Right now only rss is supported in widgets. Change this as per type of widgets in the future
            relative_path = CONTENT_THUMBNAILS['rss']
        else:
            relative_path = CONTENT_THUMBNAILS['url']
        return relative_path

    @property
    def thumbnail_url(self):
        relative_path = self.thumbnail_relative_path()
        return MEDIA_HOST + relative_path

    @property
    def thumbnail_path(self):
        return os.path.join(BASE_DIR, self.thumbnail_relative_path())

    def get_url(self):
        if self.document:
            return MEDIA_HOST + self.document.url
        elif self.is_folder:
            return ''
        elif self.is_fb_widget:
            return MEDIA_HOST + '/api/content/getFbWidget/'
        elif self.is_text_scroll_widget:
            return ''
        else:
            return self.url

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Content.objects.select_related('content_type').filter(organization=user_details.organization)

    @staticmethod
    def get_user_widgets(user_details):
        return Content.objects.select_related('content_type').filter(
            Q(organization=user_details.organization) | Q(organization__isnull=True)).filter(
            content_type__file_type__icontains='widget')

    # This includes both files, folders and URLs
    @staticmethod
    def get_user_filesystem(user_details):
        return Content.get_user_relevant_objects(user_details=user_details).exclude(
            content_type__file_type__icontains='widget')

    def save_relevant_playlists(self):
        debugFileLog.info('save_relevant_playlists')
        try:
            from playlistManagement.models import PlaylistItems
            playlist_items = PlaylistItems.objects.filter(content_id=self.content_id)
            for item in playlist_items:
                item.playlist.save()
        except Exception as e:
            debugFileLog.exception("Exception while saving the playlist to update relevant schedules")
            mail_exception(exception=e)

    def get_user_invisible_playlist_items(self):
        try:
            self.playlist_items
        except AttributeError:
            self.playlist_items = []
        if self.playlist_items:
            return self.playlist_items
        else:
            from playlistManagement.models import PlaylistItems
            playlist_items = PlaylistItems.objects.select_related('playlist').filter(content_id=self.content_id,
                                                                                     playlist__user_visible=False)
            if playlist_items.exists():
                return playlist_items
            else:
                return []

    def delete_user_invisible_playlists(self):
        try:
            playlist_items = self.get_user_invisible_playlist_items()
            if playlist_items:
                for each_playlist_item in playlist_items:
                    playlist = each_playlist_item.playlist
                    playlist.delete()
        except Exception as e:
            mail_exception(exception=e)

    def get_playlist_type(self):
        from playlistManagement.models import Playlist
        if self.is_widget:
            return Playlist.WIDGET
        elif self.organization.organization_name == CONTENT_ORGANIZATION_NAME:
            return Playlist.BLYNQ_TV
        else:
            return Playlist.CONTENT

    def create_user_invisible_playlist(self):
        try:
            if self.is_folder:
                return
            from playlistManagement.models import Playlist, PlaylistItems
            playlist_type = self.get_playlist_type()
            playlist = Playlist(playlist_title=self.title, user_visible=False, playlist_type=playlist_type,
                                created_by=self.uploaded_by, last_updated_by=self.last_updated_by,
                                organization=self.organization)
            playlist.save()
            playlist_item = PlaylistItems(playlist=playlist, content=self, display_time=self.duration)
            playlist_item.save()
        except Exception as e:
            mail_exception(exception=e)

    def update_user_invisible_playlists(self):
        try:
            if self.is_folder:
                return
            playlist_items = self.get_user_invisible_playlist_items()
            for playlist_item in playlist_items:
                # Update user invisible playlist title
                playlist = playlist_item.playlist
                playlist.playlist_title = self.title
                # Below line not required after initial merge
                playlist.playlist_type = self.get_playlist_type()
                playlist.save()
        except Exception as e:
            mail_exception(exception=e)


class FbWidget(models.Model):
    default_no_of_posts = 10
    default_post_duration = 15

    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    fb_page_url = models.CharField(max_length=250)
    no_of_posts = models.IntegerField(default=default_no_of_posts)
    post_duration = models.IntegerField(default=default_post_duration)

    @staticmethod
    def get_page_name(fb_page_url):
        page_name = ''
        fb_str = 'facebook.com/'
        search_index = fb_page_url.find(fb_str)
        if search_index != -1:
            rem_page_name = fb_page_url[search_index + len(fb_str):]
            page_name = rem_page_name.split('/')[0]
        return page_name

    def __unicode__(self):
        return self.fb_page_url


class InstagramWidget(models.Model):
    default_no_of_posts = 10
    default_post_duration = 15

    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    no_of_posts = models.IntegerField(default=default_no_of_posts)
    post_duration = models.IntegerField(default=default_post_duration)

    def __unicode__(self):
        return self.content.title


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
