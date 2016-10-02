from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from customLibrary.views_lib import debugFileLog
from layoutManagement.models import Layout


@receiver(post_save, sender=Layout)
def post_save_layout(sender, instance, **kwargs):
    debugFileLog.info("inside post_save_layout")
    from scheduleManagement.models import Schedule
    layout_schedules = Schedule.objects.filter(layout_id=instance.layout_id)
    for each_schedule in layout_schedules:
        each_schedule.update_screens_data()


@receiver(pre_delete, sender=Layout)
def remove_layout(sender, instance, **kwargs):
    if instance.is_default:
        raise Exception('Cannot delete the default Full Screen layout')
    from scheduleManagement.models import Schedule
    schedules = Schedule.objects.filter(layout=instance)
    if schedules:
        raise Exception('Cannot delete layout as it is already in use')
