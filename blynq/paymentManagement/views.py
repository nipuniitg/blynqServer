from django.core.exceptions import ObjectDoesNotExist
from customLibrary.views_lib import get_userdetails, mail_exception
from paymentManagement.models import PaymentDueMessage
from paymentManagement.serializers import default_payment_due_serializer


def payment_warning_dict(request):
    json_dict = {}
    try:
        user_details = get_userdetails(request)
        payment_due = PaymentDueMessage.objects.get(organization=user_details.organization)
        json_dict = default_payment_due_serializer([payment_due])[0]
    except ObjectDoesNotExist:
        pass
    except Exception as e:
        mail_exception(exception=e)
    return json_dict
