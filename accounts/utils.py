import email
from math import e
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from collegenotes.accounts.emails import send_email

def send_verification_email(request, user, token):
    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={'token': token})
    )

    subject = 'Verify your email'
    message = f'''
Hi {user.username},

Please verify your email by clicking the link below:

{activation_link}
'''

    send_email(
        to=[email],
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )