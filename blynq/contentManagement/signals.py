import os
import shutil

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from blynq.settings import DELETED_CONTENT_DIR, MEDIA_ROOT
from contentManagement.models import Content, FbWidget
from customLibrary.custom_settings import PERMANENTLY_DELETE_FILES
from customLibrary.views_lib import debugFileLog, mail_exception


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
                    mail_exception(exception=e)
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
                    mail_exception(exception=e)
        else:
            error = "To be deleted content %s does not exist" % file_src
            mail_exception(error)
    except Exception as e:
        mail_exception(exception=e)


@receiver(post_save, sender=Content)
def post_save_content(sender, instance, **kwargs):
    debugFileLog.info("inside post_save_content")
    instance.save_relevant_playlists()
    instance.update_user_invisible_playlists()


@receiver(pre_delete, sender=Content)
def pre_delete_content(sender, instance, **kwargs):
    debugFileLog.info("inside pre_delete_content")
    instance.decrement_size()
    instance.delete_user_invisible_playlists()
    instance.save_relevant_playlists()


@receiver(post_delete, sender=Content)
def post_delete_content(sender, instance, **kwargs):
    debugFileLog.info("inside post_delete_content")
    if instance.document:
        delete_actual_file(instance)


@receiver(post_save, sender=FbWidget)
def post_fb_widget_save(sender, instance, **kwargs):
    debugFileLog.info("inside post_fb_widget_save")
    num_of_loops = 5
    try:
        relevant_content = instance.content
        refresh_time = num_of_loops * instance.no_of_posts * instance.post_duration
        relevant_content.duration = refresh_time
        relevant_content.save()
    except Exception as e:
        debugFileLog.error("Error while updating the default duration of content for Fb widget %s" % str(instance.fb_page_url))
        debugFileLog.exception(e)
