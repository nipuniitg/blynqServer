from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from schedule.models import Calendar
from authentication.models import Organization, UserDetails, City
from customLibrary.views_lib import debugFileLog
# Create your models here.


# Possible screen status
# Unactivated - Need to enter the activation key
# Online - The device is on and displaying advertisements
# Idle - The device is on but not displayng advertisements
# Offline - The device is down or not connected to internet

class ScreenStatus(models.Model):
    screen_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.status_name

    def natural_key(self):
        return self.status_name


# class BusinessType(models.Model):
#     type_name = models.CharField(max_length=50)
#     description = models.TextField()
#
#     def __unicode__(self):
#         return self.type_name


# class ScreenSpecs(models.Model):
#     screen_specs_id = models.AutoField(primary_key=True)
#     brand = models.CharField(max_length=50)
#     model_num = models.CharField(max_length=50, null=True, blank=True)
#     weight = models.FloatField(null=True, blank=True)    # in kgs
#     dimensions = models.CharField(max_length=50, null=True, blank=True)    # l*b*h in cm
#     display_type = models.CharField(max_length=10, null=True, blank=True)  # LED/ LCD etc
#     contrast_ratio = models.CharField(max_length=20, null=True, blank=True)
#     wattage = models.IntegerField(null=True, blank=True)  # 55 in watts
#     additional_details = models.TextField(null=True, blank=True)
#
#     def __unicode__(self):
#         return self.brand + ' ' + self.model_num
#
#     class Meta:
#         unique_together = ('brand', 'model_num')
#
#     def natural_key(self):
#         return self.brand, self.model_num, self.display_type


class ScreenActivationKey(models.Model):
    screen_activation_id = models.AutoField(primary_key=True)
    activation_key = models.CharField(max_length=16, unique=True)
    device_serial_num = models.CharField(max_length=20, unique=True, null=True, blank=True)
    in_use = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return 'serial number {0} key {1}'.format(str(self.device_serial_num), str(self.activation_key))


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    # TODO: When a manager deletes the below user, set his info here
    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='%(class)s_created_by')
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='%(class)s_last_updated_by')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created_on', 'group_name')

    def __unicode__(self):
        return self.group_name

    def natural_key(self):
        return ({'group_id': self.group_id, 'group_name': self.group_name})

    # Only used once, try to refractor more code using functions like this
    @staticmethod
    def get_user_relevant_objects(user_details):
        return Group.objects.filter(organization=user_details.organization)


class GroupScreens(models.Model):
    group_screen_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True,
                                   related_name='%(class)s_created_by')

    def __unicode__(self):
        return self.screen.screen_name + '-' + self.group.group_name


class Screen(models.Model):
    screen_id = models.AutoField(primary_key=True)
    screen_name = models.CharField(max_length=100)
    screen_size = models.IntegerField(blank=True, null=True)  # in inches
    aspect_ratio = models.CharField(max_length=20, null=True, blank=True)
    resolution = models.CharField(max_length=20, null=True, blank=True)  # 1366*768
    # specifications = models.ForeignKey(ScreenSpecs, on_delete=models.PROTECT, null=True, blank=True)

    # TODO: change this location to a foreign key to authentication.Address
    # location = models.ForeignKey(Address, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True)
    city = models.ForeignKey(City, blank=True, null=True)

    unique_device_key = models.OneToOneField(ScreenActivationKey)
    activated_on = models.DateTimeField(auto_now_add=True)
    activated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='%(class)s_activated_by')
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='%(class)s_last_updated_by')
    # related_name - The name to use for the relation from the related object back to this one
    # placed_by - the organization which is keeping the screens
    # placed_by = models.ForeignKey(Organization, on_delete=models.PROTECT,related_name='%(class)s_placed_by', blank=True, null=True)
    # owned_by - the organization which is currently owning the screens. Set this value to 'Blynq',
    # to have public access for all the companies and also for advertising different companies in slots.
    owned_by = models.ForeignKey(Organization, null=True)

    BUSINESS_TYPE_CHOICES = (
        ('PRIVATE', 'The screens is bought for private use.'),
        ('PUBLIC-PRIVATE', 'Only one organization can display advertisement on this screen.'),
        ('PUBLIC-SHARED', 'Multiple organization can display advertisement on this screen in slots.'),
    )
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default=BUSINESS_TYPE_CHOICES[0][0])

    status = models.ForeignKey(ScreenStatus, on_delete=models.PROTECT, null=True)
    groups = models.ManyToManyField(Group, blank=True, through=GroupScreens)

    # Each screen should have a separate calendar
    # Remove null=True for screen_calendar
    screen_calendar = models.ForeignKey(Calendar, on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.screen_name

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Screen.objects.filter(owned_by=user_details.organization)


@receiver(post_save, sender=GroupScreens)
def create_schedule_screens(sender, instance, **kwargs):
    debugFileLog.info("Inside create_schedule_screens post_save")
    screen = instance.screen
    group = instance.group
    from scheduleManagement.models import ScheduleScreens
    group_schedules = ScheduleScreens.objects.filter(screen__isnull=True, group=group)
    for each_group_schedule in group_schedules:
        screen_event = each_group_schedule.event
        screen_event.pk = None
        screen_event.calendar = screen.screen_calendar
        screen_event.save()
        ScheduleScreens.objects.create(screen=screen, schedule=each_group_schedule.schedule, group=group,
                                       event=screen_event)
    debugFileLog.info("Schedules for the group has been successfully copied to the screen")


# This function is to either remove groups from screens or screens from groups and remove relevant entries from the
# ScheduleScreens table
@receiver(pre_delete, sender=GroupScreens)
def remove_schedule_screens(sender, instance, **kwargs):
    debugFileLog.info("Inside remove_schedule_screens pre_delete")
    from scheduleManagement.models import ScheduleScreens
    schedule_screens = ScheduleScreens.objects.filter(group=instance.group, screen=instance.screen)
    schedule_screens.delete()


class ScreenPane(models.Model):
    screen_pane_id = models.AutoField(primary_key=True)
    # Change this pane_title to some pane unique identifier
    pane_title = models.CharField(max_length=100, null=True, blank=True)
    lower_x = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    lower_y = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    width = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    height = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    split_screen = models.ForeignKey('SplitScreen', null=True, blank=True, related_name='%(class)s_splitscreen')

    def __unicode__(self):
        return self.split_screen.title + '-' + self.pane_title


class SplitScreen(models.Model):
    split_screen_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    # By default we will be giving only 4 layout options:
    # layout_id -1 : For (lower_x=0, lower_y=0, width=100, height=100)
    # layout_id -2 : For (lower_x=0, lower_y=0, width=50, height=100); (lower_x=50, lower_y=0, width=50, height=100)
    # layout_id -3 : For (lower_x=0, lower_y=10, width=100, height=90); (lower_x=0, lower_y=0, width=100, height=10)
    # layout_id -4 : For (lower_x=0, lower_y=10, width=50, height=90); (lower_x=50, lower_y=10, width=50, height=90);
    # (lower_x=0, lower_y=0, width=100, height=10)
    layout_id = models.IntegerField(default=0, null=True, blank=True)
    num_of_panes = models.IntegerField(default=2)

    def __unicode__(self):
        return self.title