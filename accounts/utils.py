from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

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
