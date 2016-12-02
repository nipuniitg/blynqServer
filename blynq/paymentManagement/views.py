from django.shortcuts import render
from customLibrary.views_lib import get_userdetails
from paymentManagement.models import PaymentDueMessage


def payment_warning_dict(request):
    json_dict = {'payment_warning_message': '', 'show_warning': False}
    try:
        user_details = get_userdetails(request)
        payment_due = PaymentDueMessage.objects.get(organization=user_details.organization)
        json_dict['payment_warning_message'] = payment_due.payment_warning_message
        json_dict['show_warning'] = payment_due.show_warning
    except Exception as e:
        pass
    return json_dict