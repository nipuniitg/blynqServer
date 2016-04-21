from django.db import models
from django.conf import settings
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile

import os
import hashlib

# Create your models here.
from authentication.models import UserDetails, Organization


class ContentType(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('IMG', 'Image'),
        # Uncomment below types when we add support
        ('VID', 'Video'),
        ('PPT', 'Presentation'),
        ('PDF', 'Pdf'),
        ('GIF', 'Gif'),
    )
    type = models.CharField(max_length=3, choices=CONTENT_TYPE_CHOICES)
    fileExtension = models.CharField(max_length=5)


def upload_to_dir(instance, filename):
    return 'usercontent/%d/%s' % (instance.uploaded_by.id, filename)


def create_dir(parent_dir_path, dir_name ):
    try:
        os.mkdir(os.path.join(parent_dir_path,dir_name))
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            pass
        else:
            print "Error in os.mkdir : " % e.errno


def move_file(instance, new_file_path):
    # Ref : https://docs.djangoproject.com/en/1.8/topics/files/
    initial_path = instance.document.path
    instance.document.name = new_file_path
    new_path = settings.MEDIA_ROOT + instance.document.name
    try:
        os.rename(initial_path, new_path)
    except OSError as e:
        print "Error in os.rename : " % e.errno
    instance.save()


# class Folder(models.Model):
#     """
#     Represents a Folder that things (files) can be put into. Folders are *NOT*
#     mirrored in the Filesystem and can have any unicode chars as their name.
#     Other models may attach to a folder with a ForeignKey. If the related name
#     ends with "_files" they will automatically be listed in the
#     folder.files list along with all the other models that link to the folder
#     in this way. Make sure the linked models obey the AbstractFile interface
#     (Duck Type).
#     """
#     is_root = False
#
#     parent = models.ForeignKey('self', verbose_name=('parent'), null=True, blank=True,
#                                related_name='children')
#     name = models.CharField(_('name'), max_length=100)
#
#     owner = models.ForeignKey(UserDetails, verbose_name=('owner'),
#                               related_name='%(class)s_owner',
#                               null=True, blank=True)
#
#     uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)
#
#     created_at = models.DateTimeField(_('created at'), auto_now_add=True)
#     modified_at = models.DateTimeField(_('modified at'), auto_now=True)
#
#     # For each entry in content table, we add an entry into the Folder table and
#     # set the dummy_content_folder to True. So that it would be easy in the scheduleManagement
#     dummy_content_folder = models.BooleanField(default=False)
#
#     @property
#     def logical_path(self):
#         """
#         Gets logical path of the folder in the tree structure.
#         Used to generate breadcrumbs
#         """
#         folder_path = []
#         if self.parent:
#             folder_path.extend(self.parent.get_ancestors())
#             folder_path.append(self.parent)
#         return folder_path
#
#     @property
#     def pretty_logical_path(self):
#         return "/%s" % "/".join([f.name for f in self.logical_path + [self]])
#
#     @property
#     def quoted_logical_path(self):
#         return urlquote(self.pretty_logical_path)


class Content(models.Model):
    # This class includes both files and folders as Content
    title = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))

    document = models.FileField(upload_to=upload_to_dir, null=True)

    sha1_hash = models.CharField(_('sha1'), max_length=40, blank=True, default='')
    original_filename = models.CharField(_('original filename'), max_length=100, blank=True, null=True)
    file_type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT)

    # folder = models.ForeignKey(Folder, verbose_name=_('folder'), related_name='all_files',
    #                            null=True, blank=True)

    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_uploaded_by')
    uploaded_time = models.DateTimeField(_('uploaded time'), auto_now_add=True)

    last_modified_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_modified_by')
    last_modified_time = models.DateTimeField(_('modified at'), auto_now=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    # is_inside = null implies the files are in the home directory of the user
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    is_folder = models.BooleanField(default=False)

    # TODO: call logical_path to update this relative_path when a Content object is created or modified
    relative_path = models.CharField(max_length=1025, default='/')

    def logical_path(self):
        path = '/'
        instance = self
        while instance.parent_folder:
            path = [instance.parent_folder.title] + '/' + path
            instance = instance.parent_folder
        return path

    class Meta:
        # unique_together = (('title', 'folder', 'uploaded_by'))
        unique_together = (('title', 'parent_folder', 'uploaded_by'))


    # def _move_file(self, dst_file_name ):
    #     """
    #     Move the file from src to dst.
    #     """
    #     # TODO : Validate the dst_file_name
    #
    #     src_file_name = self.document.name
    #     # dst_file_name = self._meta.get_field('file').generate_filename(
    #     #     self, self.original_filename)
    #     storage = self.document.storage
    #     src_file = storage.open(src_file_name)
    #     src_file.open()
    #     self.document = storage.save(dst_file_name,
    #         ContentFile(src_file.read()))
    #     storage.delete(src_file_name)
    #
    # def _copy_file(self, destination, overwrite=False):
    #     """
    #     Copies the file to a destination files and returns it.
    #     """
    #
    #     if overwrite:
    #         # If the destination file already exists default storage backend
    #         # does not overwrite it but generates another filename.
    #         # TODO: Find a way to override this behavior.
    #         raise NotImplementedError
    #
    #     src_file_name = self.document.name
    #     storage = self.document.storage
    #
    #     # This is needed because most of the remote File Storage backend do not
    #     # open the file.
    #     src_file = storage.open(src_file_name)
    #     src_file.open()
    #     return storage.save(destination, ContentFile(src_file.read()))
    #
    # def generate_sha1(self):
    #     sha = hashlib.sha1()
    #     self.document.seek(0)
    #     while True:
    #         buf = self.document.read(104857600)
    #         if not buf:
    #             break
    #         sha.update(buf)
    #     self.sha1 = sha.hexdigest()
    #     # to make sure later operations can read the whole file
    #     self.document.seek(0)
    #
    # @property
    # def path(self):
    #     try:
    #         return self.document.path
    #     except:
    #         return ""
    #
    # @property
    # def size(self):
    #     return self._file_size or 0
    #
    # def save(self, *args, **kwargs):
    #     # cache the file size
    #     # TODO: only do this if needed (depending on the storage backend the whole file will be downloaded)
    #     try:
    #         self._file_size = self.file.size
    #     except:
    #         pass
    #     # generate SHA1 hash
    #     # TODO: only do this if needed (depending on the storage backend the whole file will be downloaded)
    #     try:
    #         self.generate_sha1()
    #     except Exception:
    #         pass
    #     super(Content, self).save(*args, **kwargs)
    # save.alters_data = True
    #
    # def delete(self, *args, **kwargs):
    #     # Delete the model before the file
    #     super(Content, self).delete(*args, **kwargs)
    #     # Delete the file if there are no other Files referencing it.
    #     if not Content.objects.filter(document=self.document.name, is_public=self.is_public).exists():
    #         self.document.delete(False)
    # delete.alters_data = True

