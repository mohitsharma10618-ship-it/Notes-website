from django.contrib.auth import get_user_model
from django.conf import settings

def create_admin_once():
    # Safety check: env vars exist honi chahiye
    if not all([
        settings.ADMIN_USERNAME,
        settings.ADMIN_EMAIL,
        settings.ADMIN_PASSWORD
    ]):
        return

    User = get_user_model()

    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD
        )