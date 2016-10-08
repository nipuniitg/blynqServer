from django.apps import AppConfig


class ScheduleManagementAppConfig(AppConfig):
    name = 'scheduleManagement'

    def ready(self):
        import scheduleManagement.signals
