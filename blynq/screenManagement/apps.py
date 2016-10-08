from django.apps import AppConfig


class ScreenManagementAppConfig(AppConfig):
    name = 'screenManagement'

    def ready(self):
        import screenManagement.signals
