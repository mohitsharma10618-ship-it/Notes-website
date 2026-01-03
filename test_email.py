"""
Quick test script to check email configuration
Run: python manage.py shell < test_email.py
Or: python manage.py shell, then paste this code
"""
from django.core.mail import send_mail
from django.conf import settings

try:
    send_mail(
        subject="Test Email from StudySetU",
        message="This is a test email to verify email configuration.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["mohitsharma10618@gmail.com"],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Email failed: {str(e)}")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")

