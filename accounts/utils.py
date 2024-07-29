from email.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from accounts.models import User

def save_user(form, role):
  first_name = form.cleaned_data['first_name']
  last_name = form.cleaned_data['last_name']
  username = form.cleaned_data['username']
  email = form.cleaned_data['email']
  password = form.cleaned_data['password']
  user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
  user.role = role
  user.save()
  return user


def send_verification_email(request, user):
  domain = get_current_site(request)
  email_subject = 'Please activate your account'
  email_body = render_to_string('accounts/emails/account_verification_email.html', {
    'user': user,
    'domain': domain,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'token': default_token_generator.make_token(user),
  })
  to_email = user.email
  EmailMessage(subject=email_subject, body=email_body, to=[to_email]).send()

def detect_user(user):
  if user.role == 1:
    redirect_url = 'vendor-dashboard'
    return redirect_url
  elif user.role == 2:
    redirect_url = 'customer-dashboard'
    return redirect_url
  elif user.role == None and user.is_superuser:
    redirect_url = '/admin'
    return redirect_url
  
def vendor_required(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied
  
def customer_required(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied
  
def guest_user_only(user):
  return not user.is_authenticated
