from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from vendor.models import Vendor


def send_notification(template, email_subject, context):
  from_email = settings.DEFAULT_FROM_EMAIL
  email_body = render_to_string(template, context)
  to_email = context['user'].email
  email = EmailMessage(
      subject=email_subject,
      body=email_body,
      from_email=from_email,
      to=[to_email],
    )
  email.send()

