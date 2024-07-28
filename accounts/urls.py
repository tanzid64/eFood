from django.urls import path
from . import views

urlpatterns = [
  path('register-user/', views.register_user, name='register-user'),
  path('register-vendor/', views.register_vendor, name='register-vendor'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('dashboard/', views.dashboard, name='dashboard'),
]