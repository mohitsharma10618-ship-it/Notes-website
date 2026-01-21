from resend import Resend
from django.conf import settings

resend = Resend(api_key=settings.RESEND_API_KEY)

def send_email(to, subject, html):
    resend.emails.send({
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": to,
        "subject": subject,
        "html": html,
    })