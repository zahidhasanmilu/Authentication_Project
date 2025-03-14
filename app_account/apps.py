from django.apps import AppConfig



class AppAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_account'

    def ready(self):
        import app_account.signals  # noqa: F401