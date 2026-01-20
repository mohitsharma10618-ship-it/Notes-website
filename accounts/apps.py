from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # ensures signals are registered
        from .utils import create_admin_if_not_exists
        create_admin_if_not_exists()