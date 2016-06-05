import shutil

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
import os
import hashlib
# Create your models here.
from authentication.models import UserDetails, Organization
from blynq.settings import BASE_DIR, MEDIA_ROOT, USERCONTENT_DIR, DELETED_CONTENT_DIR
from customLibrary.views_lib import debugFileLog


# class ContentType(models.Model):
#     content_type_id = models.AutoField(primary_key=True)
#     CONTENT_TYPE_CHOICES = (
#         ('IMG', 'Image'),
#         # Uncomment below types when we add support
#         ('VID', 'Video'),
#         ('PPT', 'Presentation'),
#         ('PDF', 'Pdf'),
#         ('GIF', 'Gif'),
#     )
#     type = models.CharField(max_length=3, choices=CONTENT_TYPE_CHOICES)
#     file_extension = models.CharField(max_length=10)
#
#     def __unicode__(self):
#         return self.type + ' - ' + self.file_extension


# def create_dir(parent_dir_path, dir_name ):
#     try:
#         os.mkdir(os.path.join(parent_dir_path,dir_name))
#     except OSError as e:
#         if e.errno == 17:
#             # Dir already exists. No biggie.
#             pass
#         else:
#             print "Error in os.mkdir : " % e.errno


# def move_file(instance, new_file_path):
#     # Ref : https://docs.djangoproject.com/en/1.8/topics/files/
#     initial_path = instance.document.path
#     instance.document.name = new_file_path
#     new_path = settings.MEDIA_ROOT + instance.document.name
#     try:
#         os.rename(initial_path, new_path)
#     except OSError as e:
#         print "Error in os.rename : " % e.errno
#     instance.save()


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


def upload_to_dir(instance, filename):
    return '%s/user%d/%s' % (USERCONTENT_DIR, instance.uploaded_by.id, filename)


@receiver(pre_delete)
def delete_file(sender, instance, **kwargs):
    debugFileLog.info("inside delete_file")
    if sender == Content and instance.document:
        try:
            organization = instance.organization
            organization.used_file_size = organization.used_file_size - instance.document.size
            if organization.used_file_size < 0:
                organization.used_file_size = 0
            organization.save()
        except Exception as e:
            debugFileLog.exception("Exception while subtracting the deleted file size")
        try:
            src = instance.document.url
            file_src = BASE_DIR + src
            if os.path.exists(file_src):
                dst = '%s/organization%d/' % (DELETED_CONTENT_DIR, instance.organization.organization_id)
                file_dst = os.path.join(MEDIA_ROOT, dst)
                try:
                    if not os.path.exists(file_dst):
                        os.makedirs(file_dst)
                    shutil.move(file_src, file_dst)
                except Exception as e:
                    debugFileLog.error("Error while moving deleted content to media/deletedcontent/organization_id")
                    debugFileLog.exception(e)
            else:
                debugFileLog.error("To be deleted content %s does not exist" % file_src)
        except Exception as e:
            debugFileLog.exception("Unknown exception while deleting content")
            debugFileLog.exception(e)


class Content(models.Model):
    # This class includes both files and folders as Content
    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name=_('name'))
    # description = models.TextField(null=True, blank=True, verbose_name=_('description'))

    document = models.FileField(upload_to=upload_to_dir, null=True)

    sha1_hash = models.CharField(_('sha1'), max_length=40, blank=True, default='')
    original_filename = models.CharField(_('original filename'), max_length=100, blank=True, null=True)
    # file_type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT)
    document_type = models.CharField(max_length=50, default='image/jpg', null=True)

    # folder = models.ForeignKey(Folder, verbose_name=_('folder'), related_name='all_files',
    #                            null=True, blank=True)

    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_uploaded_by',
                                    null=True)
    uploaded_time = models.DateTimeField(_('uploaded time'), auto_now_add=True)

    last_modified_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, related_name='%(class)s_modified_by',
                                         null=True)
    last_modified_time = models.DateTimeField(_('modified at'), auto_now=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    # is_inside = null implies the files are in the home directory of the user
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    is_folder = models.BooleanField(default=False)

    # TODO: call logical_path to update this relative_path when a Content object is created or modified
    relative_path = models.CharField(max_length=1025, default='/')

    def save(self, *args, **kwargs):
        if not self.document:
            self.document_type = 'folder'
            super(Content, self).save(*args, **kwargs)
        else:
            import mimetypes
            document_type, encoding = mimetypes.guess_type(self.document.name)
            self.document_type = document_type
            if self.organization.used_file_size + self.document.size <= self.organization.total_file_size_limit:
                self.organization.used_file_size = self.organization.used_file_size + self.document.size
                self.organization.save()
                super(Content, self).save(*args, **kwargs)
            else:
                debugFileLog.warning("The organization " + self.organization.name + " total file size limit exceeded")
                debugFileLog.error("Can't upload file")

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

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Content.objects.filter(organization=user_details.organization)

        # class Meta:
        #     unique_together = (('title', 'parent_folder', 'uploaded_by'))


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
