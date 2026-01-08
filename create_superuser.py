import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJ_SUPERUSER_NAME")
email = os.environ.get("DJ_SUPERUSER_EMAIL")
password = os.environ.get("DJ_SUPERUSER_PASSWORD")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superuser created!")
    else:
        print("Superuser already exists.")