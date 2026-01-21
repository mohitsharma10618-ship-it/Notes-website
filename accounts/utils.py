import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_verification_email(email, token):
    verification_link = f"{settings.FRONTEND_URL}/accounts/verify/{token}/"

    resend.Emails.send({
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": email,
        "subject": "Verify your email",
        "html": f"""
            <h2>Welcome 🎉</h2>
            <p>Click below to verify your email:</p>
            <a href="{verification_link}">Verify Email</a>
            <br><br>
            <p>If you didn't request this, ignore this email.</p>
        """
    })