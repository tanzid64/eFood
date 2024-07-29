from django.urls import path
from accounts import views as a_views
from . import views

urlpatterns = [
  path('', a_views.vendor_dashboard,),
  path('profile/', views.vendor_profile, name='vendor-profile'),
]