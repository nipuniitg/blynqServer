from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from reversion.admin import VersionAdmin
from playlistManagement.models import Playlist, PlaylistItems


class PlaylistAdmin(VersionAdmin):
    pass


class PlaylistItemsAdmin(VersionAdmin):
    pass


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(PlaylistItems, PlaylistItemsAdmin)


# Register all the models in the playlistManagement app
app = apps.get_app_config('playlistManagement')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass