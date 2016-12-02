from django.core.serializers.python import Serializer
from customLibrary.views_lib import mail_exception

__author__ = 'nipun'


def default_payment_due_serializer(query_set, fields=('show_warning', 'due_date', 'due_amount', 'payment_link',
                                                      'additional_comments')):
    return PaymentDueMessageSerializer().serialize(query_set, fields=fields, use_natural_foreign_keys=True)


class PaymentDueMessageSerializer(Serializer):
    def end_object(self, obj):
        try:
            if 'due_date' in self.selected_fields:
                self._current['due_date'] = obj.due_date.strftime('%d %b, %Y')
            self.objects.append(self._current)
        except Exception as e:
            mail_exception(exception=e)
