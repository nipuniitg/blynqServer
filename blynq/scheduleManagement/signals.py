from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from customLibrary.views_lib import debugFileLog
from scheduleManagement.models import Schedule, ScheduleScreens


@receiver(post_save, sender=Schedule)
def schedule_data_modified(sender, instance, **kwargs):
    debugFileLog.info("Inside schedule_data_modified")
    instance.update_screens_data()


@receiver(pre_delete, sender=ScheduleScreens)
def schedule_screen_data_modifed(sender, instance, **kwargs):
    debugFileLog.info("Inside schedule_screen_data_modified")
    if instance.screen:
        instance.screen.data_modified()
