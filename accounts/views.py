from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth
from accounts.utils import detect_user, save_user, send_password_reset_email, send_verification_email, vendor_required, customer_required, guest_user_only
from vendor.forms import VendorForm
# Create your views here.
@user_passes_test(guest_user_only, login_url='my-account')
def register_user(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = save_user(form, User.CUSTOMER)
      send_verification_email(request, user)
      messages.success(request, 'Your account has been registered successfully! Check your email for verification email')
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
      user = save_user(form, User.VENDOR)
      send_verification_email(request, user)
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

def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, 'Congratulations! Your account is activated')
    return redirect('my-account')
  else:
    messages.error(request, 'Invalid activation link')
    return redirect('register-user')

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

def forgot_password(request):
  if request.method == 'POST':
    email = request.POST['email']
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email__exact=email)
      # Send reset password email
      send_password_reset_email(request, user)
      messages.success(request, 'Password reset link has been sent to your email')
      return redirect('login')
    else:
      messages.error(request, 'Account does not exist')
      return redirect('forgot-password')
  return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
  pass

def reset_password(request):
  return render(request, 'accounts/reset_password.html')


