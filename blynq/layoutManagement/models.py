from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from authentication.models import Organization, UserDetails
from customLibrary.views_lib import debugFileLog
from screenManagement.models import AspectRatio


# Create your models here.


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
