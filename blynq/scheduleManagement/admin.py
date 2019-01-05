from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from scheduleManagement.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_title', 'organization', 'layout', 'get_schedule_screens', 'last_updated_time',)
    list_filter = ('organization',)
    ordering = ('-last_updated_time',)
    search_fields = ('schedule_title',)


admin.site.register(Schedule, ScheduleAdmin)

# Register all the models in the scheduleManagement app
app = apps.get_app_config('scheduleManagement')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass