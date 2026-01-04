from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# TODO: change this in production
SECRET_KEY = 'django-insecure-change-this-to-a-secure-key'

# development
DEBUG = False
ALLOWED_HOSTS = [
    "notes-website-myqz.onrender.com",
    "localhost",
    "127.0.0.1"
    ]

# apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local apps
    'accounts',
    'notes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'collegenotes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # project-level templates folder
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required for auth forms
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'collegenotes.wsgi.application'

# simple sqlite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# keep empty for dev; add validators in production
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# static files (css, js, images)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Email (use real creds or console backend for local testing)
# For development/testing, use console backend to see emails in terminal:
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# For production, use SMTP:
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "mohitsharma10618@gmail.com"
EMAIL_HOST_PASSWORD = "xywj llsj qsrs vfxr"  # Gmail App Password
DEFAULT_FROM_EMAIL = "mohitsharma10618@gmail.com"  # Use simple format for better compatibility

# media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
PROTECTED_MEDIA_ROOT = BASE_DIR / "media_protected"   # not publicly served

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# auth redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'auth-toggle'
LOGIN_URL = '/accounts/login/'
