from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.
from authentication.models import Organization
from screenManagement.models import AspectRatio


class LayoutPane(models.Model):
    layout_pane_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    left_margin = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    top_margin = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    z_index = models.IntegerField()
    width = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    height = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    layout = models.ForeignKey('Layout', null=True, blank=True, related_name='%(class)s_layout')

    def __unicode__(self):
        return self.layout.title + '-' + self.title


class Layout(models.Model):
    layout_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    aspect_ratio = models.ForeignKey(AspectRatio, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    num_of_panes = models.IntegerField(default=2)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name='%(class)s_organization')

    @staticmethod
    def get_user_relevant_objects(user_details):
        return Layout.objects.filter(organization=user_details.organization)

    def __unicode__(self):
        return self.title