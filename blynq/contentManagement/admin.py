from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from contentManagement.models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'content_type', 'get_size', 'last_updated_time', 'get_url', 'duration')
    list_filter = ('organization', )
    ordering = ('-last_updated_time', 'organization')
    search_fields = ('title', 'content_type__file_type', 'organization__organization_name')


admin.site.register(Content, ContentAdmin)


# Register all the models in the contentManagement app
app = apps.get_app_config('contentManagement')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
