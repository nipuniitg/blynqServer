from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from screenManagement.models import Screen


class ScreenAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'owned_by', 'current_status', 'last_active_time', 'app_version',
                    'get_unique_schedules_count', 'city', 'unique_device_key', )
    list_filter = ('owned_by', 'city')
    search_fields = ('screen_name', 'unique_device_key__activation_key',)
    ordering = ('-last_active_time', 'owned_by', 'app_version')


admin.site.register(Screen, ScreenAdmin)


# Register all the models in the screenManagement app
app = apps.get_app_config('screenManagement')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass