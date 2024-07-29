from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.forms import CategoryForm
from menu.models import Category, FoodItem
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.template.defaultfilters import slugify

# Create your views here.
@login_required(login_url='login')
def vendor_profile(request):
  profile = get_object_or_404(UserProfile, user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)
  if request.method == 'POST':
    profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      messages.success(request, 'Settings has been updated successfully')
      return redirect('vendor-profile')
    else:
      pass
  else:
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
  context = {
    'profile_form': profile_form,
    'vendor_form': vendor_form,
    'profile': profile,
    'vendor': vendor
  }
  return render(request, 'vendor/vendor_profile.html', context)

@login_required(login_url='login')
def menu_builder(request):
  vendor = Vendor.objects.get(user=request.user)
  categories = Category.objects.filter(vendor=vendor)
  context = {
    'categories': categories
  }
  return render(request, 'vendor/menu_builder.html')

@login_required(login_url='login')
def food_items_by_category(request, pk=None):
  vendor = Vendor.objects.get(user=request.user)
  category = get_object_or_404(Category, pk=pk)
  food_items = FoodItem.objects.filter(vendor=vendor, category=category)
  context = {
    'foodItems': food_items,
    'category': category
  }
  return render(request, 'vendor/food_items_by_category.html', context)


def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      category_name = form.cleaned_data['category_name']
      vendor = Vendor.objects.get(user=request.user)
      category = form.save(commit=False)
      category.vendor = vendor
      category.slug = slugify(category_name)
      category.save()
      messages.success(request, 'Category added successfully')
      return redirect('menu-builder')
  form = CategoryForm()
  context ={
    'form': form
  }
  return render(request, 'vendor/add_category.html', context)
