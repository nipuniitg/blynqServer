from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from customLibrary.views_lib import debugFileLog
from screenManagement.models import GroupScreens


@receiver(post_save, sender=GroupScreens)
def create_schedule_screens(sender, instance, **kwargs):
    debugFileLog.info("Inside create_schedule_screens post_save")
    screen = instance.screen
    group = instance.group
    from scheduleManagement.models import ScheduleScreens
    group_schedules = ScheduleScreens.objects.filter(screen__isnull=True, group=group)
    if group_schedules:
        screen.data_modified()
    for each_group_schedule in group_schedules:
        try:
            schedule_screen = ScheduleScreens(screen=screen, schedule=each_group_schedule.schedule, group=group)
            schedule_screen.save()
        except Exception as e:
            debugFileLog.exception("Exception while saving the Schedule Screens for screen %s group %s schedule %s" %
                                   (screen.screen_name, group.group_name, each_group_schedule.schedule.schedule_title))
    debugFileLog.info("Schedules for the group has been successfully copied to the screen")


# This function is to either remove groups from screens or screens from groups and remove relevant entries from the
# ScheduleScreens table
@receiver(pre_delete, sender=GroupScreens)
def remove_schedule_screens(sender, instance, **kwargs):
    debugFileLog.info("Inside remove_schedule_screens pre_delete")
    from scheduleManagement.models import ScheduleScreens
    schedule_screens = ScheduleScreens.objects.filter(group=instance.group, screen=instance.screen)
    if schedule_screens:
        instance.screen.data_modified()
    schedule_screens.delete()
