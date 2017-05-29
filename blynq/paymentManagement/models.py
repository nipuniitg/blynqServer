import datetime
from email.mime.application import MIMEApplication
import os
from os.path import basename
from django.db import models
from django.core.mail import EmailMessage

# Create your models here.
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item
from authentication.models import Organization, City
from blynq.settings import MEDIA_ROOT, MEDIA_URL
from customLibrary.custom_settings import INVOICE_DIR
from customLibrary.views_lib import debugFileLog
from paymentManagement.invoice_template import BlynQInvoice


class PaymentDueMessage(models.Model):
    organization = models.OneToOneField(Organization)
    show_warning = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.date.today)
    due_amount = models.FloatField(default=0)
    payment_link = models.CharField(max_length=200, blank=True, null=True)
    suspend_access = models.BooleanField(default=False)
    additional_comments = models.CharField(max_length=250, blank=True, default='')

    def __unicode__(self):
        return 'show warning: ' + str(self.show_warning) + ' ,organization: ' + str(self.organization.organization_name)


class OrganizationInvoiceInfo(models.Model):
    organization = models.ForeignKey(Organization)
    billing_name = models.CharField(max_length=250)
    billing_street = models.CharField(max_length=250, null=True, blank=True)
    billing_city = models.ForeignKey(City)
    billing_post_code = models.CharField(max_length=20)
    contact_email = models.CharField(max_length=100)

    def __unicode__(self):
        return self.organization.organization_name + ' - ' + self.billing_name


class BillingItem(models.Model):
    billing_item_id = models.AutoField(primary_key=True)
    invoice_info = models.ForeignKey(PaymentInvoice)
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=250, null=True, blank=True)
    num_of_units = models.IntegerField(default=1)
    unit_price = models.IntegerField(default=1)

    def __unicode__(self):
        return self.item_name


class PaymentInvoice(models.Model):
    payment_invoice_id = models.AutoField(primary_key=True)
    organization_info = models.ForeignKey(OrganizationInvoiceInfo)
    invoice_id = models.CharField(max_length=50, blank=True, null=True)
    payment_due_date = models.DateField(default=datetime.date.today)
    start_date = models.DateField(default=datetime.date.today)
    last_paid_date = models.DateField(null=True, blank=True)
    # is_paid = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=True)
    recurring_period = models.IntegerField(default=3)  # in months
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.organization_info)


class PaymentInfo(models.Model):
    payment_info_id = models.AutoField(primary_key=True)
    payment_invoice = models.ForeignKey(PaymentInvoice)
    start_date = models.DateField()
    end_date = models.DateField()
    invoice_url = models.CharField(max_length=250, null=True, blank=True)
    amount_paid = models.FloatField(default=0)
    amount_settled = models.BooleanField(default=False)
    slug = models.SlugField(max_length=4)

    def __unicode__(self):
        return str(self.payment_invoice)

    @property
    def invoice_id(self, invoice_datetime=None):
        invoice_datetime = invoice_datetime if invoice_datetime else self.start_date
        invoice_id = 'BLQ-' + str(1000 + self.payment_info_id) + ' / ' + invoice_datetime.strftime('%Y-%m-%d')
        return invoice_id

    @property
    def relative_path(self):
        filename = 'blynq_invoice_' + self.slug + '_' + str(self.payment_info_id) + '.pdf'
        return os.path.join(INVOICE_DIR, filename)

    def get_invoice_path(self):
        file_path = os.path.join(MEDIA_ROOT, INVOICE_DIR)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        total_filename = os.path.join(MEDIA_ROOT, self.relative_path)
        return total_filename

    def get_invoice_url(self):
        if self.invoice_url:
            return self.invoice_url
        else:
            return os.path.join(MEDIA_URL, self.relative_path)

    def create_invoice(self, invoice_datetime=None):
        try:
            if self.invoice_url:
                return
            payment_invoice = self.payment_invoice
            if not isinstance(payment_invoice, PaymentInvoice):
                return
            doc = BlynQInvoice(self.get_invoice_path())
            # Paid stamp, optional
            doc.is_paid = payment_invoice.is_paid
            invoice_datetime = invoice_datetime if invoice_datetime else datetime.datetime.now()
            doc.invoice_info = InvoiceInfo(self.invoice_id, invoice_datetime, self.start_date)  # Invoice info, optional

            doc.service_provider_info = ServiceProviderInfo(name='BlynQ Technologies Private Limited',
                                                            street='G1, Mount Fort, Pragathi Nagar', city='Hyderabad',
                                                            state='Telangana', country='India', post_code='500090')

            client_info = payment_invoice.organization_info
            client_city = client_info.billing_city
            doc.client_info = ClientInfo(name=client_info.billing_name, street=client_info.billing_street,
                                         city=client_city.city_name, state=client_city.state, country=client_city.country,
                                         post_code=client_info.billing_post_code)

            # Add Item
            billing_items = self.payment_invoice.billingitem_set.all()
            for item in billing_items:
                doc.add_item(Item(item.item_name, item.item_description, item.num_of_units, item.unit_price))
            doc.set_bottom_tip(
                "Email: hello@blynq.in   Phone: +918122846970 <br />Don't hesitate to contact us for any questions.")
            doc.finish()
            self.invoice_url = self.get_invoice_url()
            self.save()
        except Exception as e:
            debugFileLog.error(e)

    def send_reminder(self):
        subject = 'BlynQ Technologies - Please Send Payment'
        body = 'This is a friendly reminder'
        to_email = self.payment_invoice.organization_info.contact_email
        try:
            mail = EmailMessage(subject=subject, body=body, from_email='support@blynq.in',to=[to_email])
            file_path = self.get_invoice_path()
            with open(file_path, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(file_path)
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_path)
            # invoice_file = open(self.get_invoice_path())
            # mail.attach(invoice_file.name, invoice_file.read(), invoice_file.content_type)
                mail.attach(part)
            mail.send()
        except Exception as e:
            debugFileLog.error(e)