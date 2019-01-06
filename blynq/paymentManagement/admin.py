from django.apps import apps
from django.contrib import admin

# Register your models here.
# Register all the models in the current app
from django.contrib.admin.sites import AlreadyRegistered
from authentication.models import Organization
from customLibrary.views_lib import debugFileLog
from paymentManagement.models import PaymentDueMessage, CustomerSubscription, PaymentInfo, CustomerScreen


class PaymentDueMessagesAdmin(admin.ModelAdmin):
    list_display = PaymentDueMessage._meta.get_all_field_names()
    list_editable = ('show_warning', 'suspend_access',)


class CustomerScreenInline(admin.TabularInline):
    model = CustomerSubscription.screens.through

def refresh_payments(modeladmin, request, queryset):
    active_subscriptions = CustomerSubscription.objects.filter(is_active=True)
    for subscription in active_subscriptions:
        subscription.generate_payment_info()
refresh_payments.short_description = "Create New Receivables"


def add_remaining_screens_from_organization(modeladmin, request, queryset):
    for customer in queryset:
        try:
            exclude_screen_ids = CustomerScreen.objects.filter(screen__owned_by=customer.organization).values_list('screen_id', flat=True)
            remaining_screens = customer.organization.screen_set.exclude(screen_id__in=exclude_screen_ids)
            for screen in remaining_screens:
                obj, created = CustomerScreen.objects.get_or_create(screen=screen, customer=customer)
        except Exception as e:
            debugFileLog.exception(e)
add_remaining_screens_from_organization.short_description = "Add remaining screens from parent organization"


class CustomerSubscriptionAdmin(admin.ModelAdmin):
    inlines = (CustomerScreenInline,)
    actions = [add_remaining_screens_from_organization, refresh_payments]
    list_filter = (('organization', admin.RelatedOnlyFieldListFilter),)
    list_display = ('branch_name', 'get_screens_count', 'recurring_period', 'payment_start_date', 'get_cycle_amount',
                    'screen_monthly_subscription', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":
            kwargs["queryset"] = Organization.objects.filter(is_active=True)
        return super(CustomerSubscriptionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class PaymentInfoAdmin(admin.ModelAdmin):
    actions = [refresh_payments]
    list_display = ('customer', 'cycle_start_date', 'cycle_end_date', 'total_amount', 'amount_paid', 'invoice_sent',
                    'invoice_id', 'invoice', 'last_payment_date', 'last_reminder_sent', 'is_settled', 'payment_description')
    ordering = ('is_settled', 'cycle_start_date')
    list_editable = ('amount_paid', 'is_settled', 'invoice_id', 'invoice', 'invoice_sent', 'last_payment_date',
                     'last_reminder_sent', 'payment_description')

admin.site.register(PaymentDueMessage, PaymentDueMessagesAdmin)
admin.site.register(CustomerSubscription, CustomerSubscriptionAdmin)
admin.site.register(PaymentInfo, PaymentInfoAdmin)

app = apps.get_app_config('paymentManagement')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
