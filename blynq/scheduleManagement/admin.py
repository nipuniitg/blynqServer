from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from scheduleManagement.models import Schedule, SchedulePlaylists


class ScheduleAdmin(VersionAdmin):
    pass


class SchedulePlaylistsAdmin(VersionAdmin):
    pass


class ScheduleScreensAdmin(VersionAdmin):
    pass


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(SchedulePlaylists, SchedulePlaylistsAdmin)
# admin.site.register(ScheduleScreens, ScheduleScreensAdmin)


# Register all the models in the scheduleManagement app
app = apps.get_app_config('scheduleManagement')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
