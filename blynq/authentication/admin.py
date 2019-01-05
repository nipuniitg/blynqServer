from django.contrib.admin.sites import AlreadyRegistered
from authentication.models import Role, Organization, UserDetails, City
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin
from django.apps import apps


# Define an inline admin descriptor for UserDetails model
# which acts a bit like a singleton
class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'usersdetails'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserDetailsInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class OrganizationAdmin(VersionAdmin):
    list_display = ('organization_name', 'get_screen_count', 'get_latest_activity_time', 'get_file_usage', 'get_content_count', 'get_schedules_count',
                    'get_playlists_count', 'get_last_login_time')
    ordering = ('organization_name',)

admin.site.register(Organization, OrganizationAdmin)


# Register all the models in the contentManagement app
app = apps.get_app_config('authentication')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
