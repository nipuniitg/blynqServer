from django.apps import AppConfig


class LayoutManagementAppConfig(AppConfig):
    name = 'layoutManagement'

    def ready(self):
        import layoutManagement.signals
