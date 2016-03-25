from django.contrib import admin
from authentication.models import Organization, Role, UserDetails

# Register your models here.
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(UserDetails)

