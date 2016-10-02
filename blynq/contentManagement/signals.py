import os
import shutil

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from blynq.settings import DELETED_CONTENT_DIR, MEDIA_ROOT
from contentManagement.models import Content
from customLibrary.custom_settings import PERMANENTLY_DELETE_FILES
from customLibrary.views_lib import debugFileLog


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


def delete_actual_file(instance):
    try:
        debugFileLog.info("Inside delete_actual_file of %s" % instance.title)
        src = instance.document.name
        file_src = instance.file_path
        # Delete thumbnail for image
        if instance.is_image and os.path.exists(instance.thumbnail_path):
            try:
                os.remove(instance.thumbnail_path)
            except Exception as e:
                debugFileLog.exception('Deletion of thumbnail %s failed with exception %s' %
                                       (instance.thumbnail_path, str(e)))
        if os.path.exists(file_src):
            if PERMANENTLY_DELETE_FILES:
                try:
                    os.remove(file_src)
                except Exception as e:
                    debugFileLog.exception('Permanent deletion of file failed with exception')
                    debugFileLog.exception(e)
            else:
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
            debugFileLog.error("To be deleted content %s does not exist" % file_src)
    except Exception as e:
        debugFileLog.exception("Unknown exception while deleting content")
        debugFileLog.exception(e)


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
        delete_actual_file(instance)
    save_relevant_playlists(content_id=instance.content_id)
