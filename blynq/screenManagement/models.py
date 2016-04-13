from django.db import models
from authentication.models import Organization, UserDetails, Address


import random, string
# Create your models here.


# Possible screen status
# Unactivated - Need to enter the activation key
# Online - The device is on and displaying advertisements
# Idle - The device is on but not displayng advertisements
# Offline - The device is down or not connected to internet
class ScreenStatus(models.Model):
    status_name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.status_name


# class BusinessType(models.Model):
#     type_name = models.CharField(max_length=50)
#     description = models.TextField()
#
#     def __unicode__(self):
#         return self.type_name


class Group(models.Model):
    group_name = models.CharField(max_length=100,null= False)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    # For each entry in the Screen table, we add an entry in the Group table and
    # set the flag dummy_screen_group to True. So that it would be easy in the scheduleManagement
    dummy_screen_group = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_on', 'group_name')

    def __unicode__(self):
        return self.group_name

    # def get_screens(id):
    #     return Screen.Objects.all(group_id = id)


class ScreenSpecs(models.Model):
    brand = models.CharField(max_length=50)
    model_num = models.CharField(max_length=50, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)    # in kgs
    dimensions = models.CharField(max_length=50, null=True, blank=True)    # l*b*h in cm
    resolution = models.CharField(max_length=20, null=True, blank=True)    # 1366*768
    display_type = models.CharField(max_length=10, null=True, blank=True)  # LED/ LCD etc
    screen_size = models.IntegerField()    # in inches
    aspect_ratio = models.CharField(max_length=20, null=True, blank=True)
    contrast_ratio = models.CharField(max_length=20, null=True, blank=True)
    wattage = models.IntegerField(null=True, blank=True)  # 55 in watts
    additional_details = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.brand + ' ' + self.model_num + ' ' + str(self.screen_size)


class OrganizationScreen(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    screen = models.ForeignKey('Screen', on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_slot_valid = models.BooleanField()
    # time_slot should be in seconds
    time_slot = models.IntegerField(null=True)


class Screen(models.Model):
    screen_name = models.CharField(max_length=100)
    specifications = models.ForeignKey(ScreenSpecs, on_delete=models.PROTECT)
    location = models.ForeignKey(Address, on_delete=models.PROTECT)
    activation_key = models.CharField(max_length=16)
    activated_on = models.DateField(null=True, blank=True)
    activated_by = models.ForeignKey(UserDetails, null=True, blank=True)
    # related_name - The name to use for the relation from the related object back to this one
    # placed_by - the organization which is keeping the screens
    placed_by = models.ForeignKey(Organization, on_delete=models.PROTECT,related_name='%(class)s_placed_by', blank=True, null=True)
    # owned_by - the organization which is currently owning the screens. Set this value to 'Blynq',
    # to have public access for all the companies and also for advertising different companies in slots.
    owned_by = models.ManyToManyField(Organization, through=OrganizationScreen)

    BUSINESS_TYPE_CHOICES = (
        ('PRIVATE', 'The screens is bought for private use.'),
        ('PUBLIC-SINGLE', 'Only one organization can display advertisement on this screen.'),
        ('PUBLIC-SHARED', 'Multiple organization can display advertisement on this screen in slots.'),
    )
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default=BUSINESS_TYPE_CHOICES[0][0])

    status = models.ForeignKey(ScreenStatus, on_delete=models.PROTECT)
    groups = models.ManyToManyField(Group, blank=True)

    @staticmethod
    def generate_activation_key(length=16):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def __unicode__(self):
        return self.screen_name