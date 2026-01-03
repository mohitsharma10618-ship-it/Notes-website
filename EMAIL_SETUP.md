# Email Configuration Guide for StudySetU

## For Development/Testing (Recommended)

If you're having issues with email sending, use the console backend to see OTPs in your terminal:

In `collegenotes/settings.py`, change:
```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

This will print emails (including OTPs) directly to your terminal/console instead of sending them.

## For Production

Use SMTP backend with Gmail:

1. **Enable 2-Step Verification** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account → Security
   - Under "2-Step Verification", click "App passwords"
   - Generate a new app password
   - Use this password (not your regular Gmail password) in settings

3. **Settings should look like:**
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"  # 16-character app password
DEFAULT_FROM_EMAIL = "your-email@gmail.com"
```

## Common Issues

- **Authentication Failed**: Check that you're using an App Password, not your regular password
- **Connection Timeout**: Check your internet connection and firewall settings
- **550 Error**: Gmail may be blocking the connection - check Gmail security settings

## Testing Email

Run this in Django shell to test:
```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject="Test",
    message="Test message",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=["your-email@gmail.com"],
)
```

