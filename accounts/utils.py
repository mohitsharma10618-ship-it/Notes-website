from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_admin_once(request):
    User = get_user_model()

    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Admin already exists")

    if not all([
        settings.ADMIN_USERNAME,
        settings.ADMIN_EMAIL,
        settings.ADMIN_PASSWORD
    ]):
        return HttpResponse("Admin env vars missing", status=500)

    User.objects.create_superuser(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD
    )

    return HttpResponse("Admin created successfully")