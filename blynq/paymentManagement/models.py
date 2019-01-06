import datetime
import os
from dateutil.relativedelta import relativedelta
from django.db import models

# Create your models here.
from authentication.models import Organization
from blynq.settings import MEDIA_ROOT
from customLibrary.custom_settings import INVOICE_UPLOAD_DIR
from customLibrary.views_lib import debugFileLog
from screenManagement.models import Screen


class PaymentDueMessage(models.Model):
    organization = models.OneToOneField(Organization)
    show_warning = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.date.today)
    due_amount = models.FloatField(default=0)
    payment_link = models.CharField(max_length=200, blank=True, null=True)
    suspend_access = models.BooleanField(default=False)
    additional_comments = models.CharField(max_length=250, blank=True, default='')

    def __unicode__(self):
        return str(self.organization.organization_name) + ' Warning: ' + str(self.show_warning) + ' , No Access: ' + str(self.suspend_access)


class CustomerSubscription(models.Model):
    customer_subscription_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100, help_text='Branch & Lot Name: Screens with different start dates should be created separately')
    additional_details = models.TextField(blank=True, null=True)
    screens = models.ManyToManyField(Screen, through='CustomerScreen')
    screen_monthly_subscription = models.IntegerField(default=500)
    payment_start_date = models.DateField()
    recurring_period = models.IntegerField(verbose_name='Recurring period in months', default=6)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    last_updated_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.branch_name

    def generate_payment_info(self, for_future_months=None):
        if not self.is_active:
            return

        if for_future_months is None:
            for_future_months = self.recurring_period

        final_date = datetime.date.today() + relativedelta(months=+for_future_months)
        cur_date = self.payment_start_date
        existing_infos = self.paymentinfo_set
        total_amount = self.get_cycle_amount()
        while cur_date <= final_date:
            try:
                p_dict = dict(total_amount=total_amount,
                              payment_description=self.generate_payment_description(cur_date))
                pinfo, created = existing_infos.get_or_create(cycle_start_date=cur_date, defaults=p_dict)
            except Exception as e:
                debugFileLog.exception(e)
            cur_date = cur_date + relativedelta(months=+self.recurring_period)

    def get_screens_count(self):
        return self.screens.filter(owned_by=self.organization).count()
    get_screens_count.short_description = 'Screens'

    def get_cycle_amount(self):
        return self.get_screens_count() * self.screen_monthly_subscription * self.recurring_period
    get_cycle_amount.short_description = 'Recurring Amount'

    def generate_payment_description(self, cur_date):
        desc_str = str(self.recurring_period) + ' months Software Subscription'
        desc_str += '(' + str(cur_date) + ' - ' + str(cur_date + relativedelta(months=self.recurring_period)) + '), '
        # desc_str += 'QTY: ' + str(self.get_screens_count()) + ', Cost: ' + str(self.screen_monthly_subscription) + ', '
        # desc_str += 'Amount: ' + str(self.get_cycle_amount())
        return desc_str


class CustomerScreen(models.Model):
    customer_screen_id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerSubscription, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.customer.branch_name + ' - ' + self.screen.screen_name


def upload_to_invoice_dir(instance, full_filename):
    filename = os.path.basename(full_filename)
    updates_dir = os.path.join(MEDIA_ROOT, INVOICE_UPLOAD_DIR)
    if not os.path.exists(updates_dir):
        os.makedirs(updates_dir)
    return '%s/%s' % (INVOICE_UPLOAD_DIR, filename)


class PaymentInfo(models.Model):
    payment_info_id = models.AutoField(primary_key=True)
    payment_description = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(CustomerSubscription, on_delete=models.CASCADE)
    cycle_start_date = models.DateField()
    total_amount = models.FloatField()
    amount_paid = models.FloatField(default=0)
    is_settled = models.BooleanField(default=False)

    invoice_id = models.CharField(max_length=50, blank=True, null=True)
    invoice = models.FileField(upload_to=upload_to_invoice_dir, null=True, blank=True)

    invoice_sent = models.BooleanField(default=False)

    last_payment_date = models.DateField(blank=True, null=True)
    last_reminder_sent = models.DateField(blank=True, null=True)

    last_updated_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.payment_description

    def cycle_end_date(self):
        return self.cycle_start_date + relativedelta(months=+self.customer.recurring_period)
    cycle_end_date.short_description = 'Cycle End Date'