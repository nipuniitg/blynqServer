from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from screenManagement.models import Screen


class ScreenAdmin(VersionAdmin):
    pass


admin.site.register(Screen, ScreenAdmin)


# Register all the models in the screenManagement app
app = apps.get_app_config('screenManagement')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass