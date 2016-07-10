from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from screenManagement.models import Group, Screen, GroupScreens


class GroupAdmin(VersionAdmin):
    pass


class ScreenAdmin(VersionAdmin):
    pass


class GroupScreensAdmin(VersionAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(GroupScreens, GroupScreensAdmin)


# Register all the models in the screenManagement app
app = apps.get_app_config('screenManagement')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass