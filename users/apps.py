from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        """
        Import auto profile creation signals upon User instance.
        """
        import users.signals
