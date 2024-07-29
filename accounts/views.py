from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth
from accounts.utils import detect_user, save_user, send_verification_email, vendor_required, customer_required, guest_user_only
from vendor.forms import VendorForm
from django.template.defaultfilters import slugify
# Create your views here.
@user_passes_test(guest_user_only, login_url='my-account')
def register_user(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = save_user(form, User.CUSTOMER)
      email_subject = 'Please activate your account'
      template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request, user, email_subject, template)
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
      email_subject = 'Please activate your account'
      template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request, user, email_subject, template)
      vendor_name = v_form.cleaned_data['vendor_name']
      vendor = v_form.save(commit=False)
      vendor.vendor_slug = slugify(vendor_name)
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
  return render(request, 'accounts/vendor-dashboard.html')

def forgot_password(request):
  if request.method == 'POST':
    email = request.POST['email']
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email__exact=email)
      # Send reset password email
      email_subject = 'eFood: Reset your password'
      template = 'accounts/emails/reset_password_email.html'
      send_verification_email(request, user, email_subject, template)
      messages.success(request, 'Password reset link has been sent to your email')
      return redirect('login')
    else:
      messages.error(request, 'Account does not exist')
      return redirect('forgot-password')
  return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    messages.info(request, 'Please reset your password')
    return redirect('reset-password')
  else:
    messages.error(request, 'This link has been expired')
    return redirect('forgot-password')

def reset_password(request):
  if request.method == 'POST':
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    if password == confirm_password:
      uid = request.session.get('uid')
      user = User.objects.get(pk=uid)
      user.set_password(password)
      user.is_active = True
      user.save()
      messages.success(request, 'Password reset successful')
      return redirect('login')
    else:
      messages.error(request, 'Password do not match')
      return redirect('reset-password')
  return render(request, 'accounts/reset_password.html')


