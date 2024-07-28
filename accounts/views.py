from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth
from accounts.utils import detect_user, vendor_required, customer_required, guest_user_only
from vendor.forms import VendorForm
# Create your views here.
@user_passes_test(guest_user_only, login_url='my-account')
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

@user_passes_test(guest_user_only, login_url='my-account')
def register_vendor(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST, request.FILES)
    if form.is_valid() and v_form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
      user.role = User.VENDOR
      user.save()
      vendor = v_form.save(commit=False)
      vendor.user = user
      user_profile = UserProfile.objects.get(user=user)
      vendor.user_profile = user_profile
      vendor.save()
      messages.success(request, 'Your account has been registered successfully! Please wait for the approval from the admin')
      return redirect('register-vendor')
    else:
      pass
  else:
    form = UserForm()
    v_form = VendorForm()
  context = {
    'form': form,
    'v_form': v_form
  }
  return render(request, 'accounts/register_vendor.html', context)

@user_passes_test(guest_user_only, login_url='my-account')
def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(email=email, password=password)
    if user:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('my-account')
    else:
      messages.error(request, 'Invalid login credentials')
      return redirect('login')
  return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  messages.info(request, 'You are logged out')
  return redirect('login')

@login_required(login_url='login')
def my_account(request):
  user = request.user
  redirect_url = detect_user(user)
  return redirect(redirect_url)

@login_required(login_url='login')
@user_passes_test(customer_required)
def customer_dashboard(request):
  return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
@user_passes_test(vendor_required)
def vendor_dashboard(request):
  return render(request, 'accounts/dashboard.html')

