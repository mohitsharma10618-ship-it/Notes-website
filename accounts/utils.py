from django.conf import settings
from django.contrib.auth import get_user_model

def create_admin_if_not_exists():
    User = get_user_model()

    if User.objects.filter(is_superuser=True).exists():
        return

    if not all([
        settings.ADMIN_USERNAME,
        settings.ADMIN_EMAIL,
        settings.ADMIN_PASSWORD
    ]):
        return

    User.objects.create_superuser(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD
    )