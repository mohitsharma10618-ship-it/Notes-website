from django.urls import reverse

from accounts.emails import send_email

def send_verification_email(request, user, token):
    activation_link = request.build_absolute_uri(
        reverse('verify-email', kwargs={'token': token})
    )

    subject = "Verify your email"

    html = f"""
    <p>Hi {user.username},</p>
    <p>Please verify your email by clicking the link below:</p>
    <p><a href="{activation_link}">Verify Email</a></p>
    """

    send_email(
        to=[user.email],
        subject=subject,
        html=html
    )