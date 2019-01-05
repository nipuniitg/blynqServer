from django.apps import apps
from django.contrib import admin

# Register your models here.
# Register all the models in the current app
from django.contrib.admin.sites import AlreadyRegistered
from paymentManagement.models import PaymentDueMessage


class PaymentDueMessagesAdmin(admin.ModelAdmin):
    list_display = PaymentDueMessage._meta.get_all_field_names()
    list_editable = ('show_warning', 'suspend_access',)


admin.site.register(PaymentDueMessage, PaymentDueMessagesAdmin)

app = apps.get_app_config('paymentManagement')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
