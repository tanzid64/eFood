from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def guest_user_only(view_func):
  def _wrapped_view_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('dashboard')
    return view_func(request, *args, **kwargs)
  return _wrapped_view_func