import html
import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_email(*,to, subject, html):
    resend.Emails.send({
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": [to],
        "subject": subject,
        "html": html,
    })