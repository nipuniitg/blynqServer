from django.core.validators import MaxValueValidator
from django.db import models

from django.utils.translation import ugettext_lazy as _


# Create your models here.
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from authentication.models import Organization, UserDetails
from customLibrary.views_lib import debugFileLog
from screenManagement.models import AspectRatio


class LayoutPane(models.Model):
    layout_pane_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    left_margin = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    top_margin = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    z_index = models.IntegerField()
    width = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    height = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    layout = models.ForeignKey('Layout', on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_layout')

    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.layout.title + '-' + self.title


class Layout(models.Model):
    layout_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    aspect_ratio = models.ForeignKey(AspectRatio, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name='%(class)s_organization')

    created_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True, blank=True, null=True)
    last_updated_by = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True,
                                        related_name='%(class)s_last_updated_by')
    last_updated_time = models.DateTimeField(_('updated time'), auto_now=True, null=True, blank=True)

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Layout.objects.filter(organization=user_details.organization)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['layout_id']


@receiver(post_save, sender=Layout)
def post_save_layout(sender, instance, **kwargs):
    debugFileLog.info("inside post_save_layout")
    from scheduleManagement.models import Schedule
    layout_schedules = Schedule.objects.filter(deleted=False, layout_id=instance.layout_id)
    for each_schedule in layout_schedules:
        each_schedule.save()


@receiver(pre_delete, sender=Layout)
def remove_layout(sender, instance, **kwargs):
    if instance.is_default:
        raise Exception('Cannot delete the default Full Screen layout')
    from scheduleManagement.models import Schedule
    schedules = Schedule.objects.filter(layout=instance, deleted=False)
    if schedules:
        raise Exception('Cannot delete layout as it is already in use')
