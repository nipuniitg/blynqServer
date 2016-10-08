from django.apps import AppConfig


class PlaylistManagementAppConfig(AppConfig):
    name = 'playlistManagement'

    def ready(self):
        import playlistManagement.signals
