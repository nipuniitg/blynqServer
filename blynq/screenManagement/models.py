from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from schedule.models import Calendar

from authentication.models import Organization, UserDetails, City
from customLibrary.custom_settings import PLAYER_INACTIVE_THRESHOLD
from customLibrary.views_lib import debugFileLog

# Create your models here.
ORIENTATION_CHOICES = (
    ('LANDSCAPE', 'Landscape Orientation'),
    ('PORTRAIT', 'Portrait Orientation'),
)


class AspectRatio(models.Model):
    aspect_ratio_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    orientation = models.CharField(max_length=20, choices=ORIENTATION_CHOICES, default=ORIENTATION_CHOICES[0][0])
    width_component = models.IntegerField()
    height_component = models.IntegerField()

    def __unicode__(self):
        return self.title


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

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

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
        return {'group_id': self.group_id, 'group_name': self.group_name}

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

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)


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

    last_active_time = models.DateTimeField(default=timezone.now)

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

    @property
    def current_status(self):
        if (timezone.now() - self.last_active_time).total_seconds() > PLAYER_INACTIVE_THRESHOLD:
            return 'Offline'
        else:
            return 'Online'

    def update_status(self):
        self.last_active_time = timezone.now()
        self.save()

    def data_modified(self):
        try:
            screen_data_modified = self.screen_data_modified
            screen_data_modified.save()
        except ScreenDataModified.DoesNotExist:
            screen_data_modified = ScreenDataModified(screen_id=self.screen_id)
            screen_data_modified.save()
        except Exception as e:
            debugFileLog.error('Received exception while updating screen data_modified %s' % self.screen_name)
            debugFileLog.error(e)

    def is_data_modified(self, last_received_datetime):
        try:
            if self.screen_data_modified.last_updated_time >= last_received_datetime:
                return True
            else:
                return False
        except Exception as e:
            debugFileLog.exception('Screen %s is_data_modified failed with exception %s ' % (self.screen_name, str(e)))
            return True


# Update the last_updated_time of a screen whenever any schedule or playlist or group or layout related to screen is
# modified. This model instance will be used in the get_screen_data function in playerManagement/views.py
class ScreenDataModified(models.Model):
    screen = models.OneToOneField(Screen, related_name='screen_data_modified', on_delete=models.CASCADE)
    last_updated_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.screen.screen_name + ' last modified at ' + str(self.last_updated_time)
