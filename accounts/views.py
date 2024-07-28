from django.shortcuts import redirect, render
from accounts.forms import UserForm
from accounts.models import User
from django.contrib import messages
# Create your views here.
def register_user(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
      user.role = User.CUSTOMER
      user.save()
      messages.success(request, 'Your account has been registered successfully! You are now able to log in')
      return redirect('register-user')
    else:
      pass
  else:
    form = UserForm()
    context = {
      'form': form
    }
  return render(request, 'accounts/register_user.html', context)