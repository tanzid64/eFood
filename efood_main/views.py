from django.shortcuts import render


def home(request):
  return render(request, 'efood_main/home.html')