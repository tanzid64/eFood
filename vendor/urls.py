from django.urls import path
from accounts import views as a_views
from . import views

urlpatterns = [
  path('', a_views.vendor_dashboard,),
  path('profile/', views.vendor_profile, name='vendor-profile'),
  path('menu-builder/', views.menu_builder, name='menu-builder'),
  path('menu-builder/category/<int:pk>/', views.food_items_by_category, name='food-items-by-category'),
  # Category CRUD
  path('menu-builder/category/add/', views.add_category, name='add-category'),
]