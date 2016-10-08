from django.apps import AppConfig


class ContentManagementAppConfig(AppConfig):
    name = 'contentManagement'

    def ready(self):
        import contentManagement.signals
