from authentication.models import Role, Organization, UserDetails, City
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin


# Define an inline admin descriptor for UserDetails model
# which acts a bit like a singleton
class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'usersdetails'


# Define a new User admin
class UserAdmin(BaseUserAdmin, VersionAdmin):
    inlines = (UserDetailsInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class OrganizationAdmin(VersionAdmin):
    pass


class RoleAdmin(VersionAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role)
admin.site.register(City)
