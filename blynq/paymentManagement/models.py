from django.db import models

# Create your models here.
from authentication.models import Organization


class PaymentDueMessage(models.Model):
    organization = models.OneToOneField(Organization)
    show_warning = models.BooleanField(default=False)
    payment_warning_message = models.CharField(max_length=250, blank=True, default='')

    def __unicode__(self):
        return 'show warning: ' + str(self.show_warning) + ' ,message: ' + str(self.payment_warning_message)
