import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from paymentManagement.models import PaymentInvoice, PaymentInfo

__author__ = 'nipun'


def generate_payment_info():
    payment_invoices = PaymentInvoice.objects.filter(is_active=True)
    for invoice in payment_invoices:
        cur_start_date = invoice.start_date
        while cur_start_date < datetime.now().date():
            cur_end_date = cur_start_date + relativedelta(months=invoice.recurring_period)
            payment_info, created = PaymentInfo.objects.get_or_create(
                payment_invoice=invoice, start_date=cur_start_date, end_date=cur_end_date)
            if not payment_info.amount_settled:
                payment_info.create_invoice()
            cur_start_date = cur_end_date


def send_invoice_reminders():
    generate_payment_info()
    payment_infos = PaymentInfo.objects.filter(amount_settled=False)
    for info in payment_infos:
        info.send_reminder()