from django.db import models
from authentication.models import Organization, UserDetails

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=100,null= False)
    description = models.TextField()
    created_on = models.DateField()
    created_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created_on', 'name')

    def __unicode__(self):
        return self.group_name

    def get_screens(id):
        return Screen.Objects.all(group_id = id)


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


class Address(models.Model):
    building_name = models.CharField(max_length=100)
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    pincode = models.IntegerField()


class ScreenSpecs(models.Model):
    brand = models.CharField(max_length=50, null=True)
    model_num = models.CharField(max_length=50, null=True)
    weight = models.FloatField(null=True)    # in kgs
    dimensions = models.CharField(max_length=50, null=True)    # l*b*h in cm
    resolution = models.CharField(max_length=20)    # 1366*768
    display_type = models.CharField(max_length=10, null=True)  # LED/ LCD etc
    size = models.IntegerField()    # in inches
    aspect_ratio = models.CharField(max_length=20, null=True)
    contrast_ratio = models.CharField(max_length=20, null=True)
    wattage = models.IntegerField(null=True)  # 55 in watts
    additional_details = models.TextField(null=True)


class ScreenStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class BusinessType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class OrganizationScreen(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    screen = models.ForeignKey('Screen', on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_slot_valid = models.BooleanField()
    # time_slot should be in seconds
    time_slot = models.IntegerField(null=True)


class Screen(models.Model):
    screen_name = models.CharField(max_length=100, null=False)
    specs = models.ForeignKey(ScreenSpecs, on_delete=models.PROTECT)
    location = models.ForeignKey(Address, on_delete=models.PROTECT)
    activation_key = models.CharField(max_length=16)
    activated_on = models.DateField()
    # related_name - The name to use for the relation from the related object back to this one
    # placed_by - the organization which is keeping the screens
    placed_by = models.ForeignKey(Organization, on_delete=models.PROTECT,related_name='%(class)s_placed_by')
    # owned_by - the organization which is currently owning the screens. Set this value to 'Blynq',
    # to have public access for all the companies and also for advertising different companies in slots.
    owned_by = models.ManyToManyField(Organization, through=OrganizationScreen)
    business_type = models.ForeignKey(BusinessType, on_delete=models.PROTECT)
    status = models.ForeignKey(ScreenStatus, on_delete=models.PROTECT)
    groups = models.ManyToManyField(Group)


    def __unicode__(self):
        return self.screen_name



