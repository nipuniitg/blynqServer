import datetime
from django.db import models

# Create your models here.
from authentication.models import Organization


class PaymentDueMessage(models.Model):
    organization = models.OneToOneField(Organization)
    show_warning = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.date.today)
    due_amount = models.FloatField(default=0)
    payment_link = models.CharField(max_length=200, blank=True, null=True)
    additional_comments = models.CharField(max_length=250, blank=True, default='')

    def __unicode__(self):
        return 'show warning: ' + str(self.show_warning) + ' ,organization: ' + str(self.organization.organization_name)
