from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from contentManagement.models import Content, ContentType


class ContentAdmin(VersionAdmin):
    pass


admin.site.register(Content, ContentAdmin)
admin.site.register(ContentType)


# Register all the models in the contentManagement app
app = apps.get_app_config('contentManagement')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
