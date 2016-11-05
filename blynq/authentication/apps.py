from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        import authentication.signals
