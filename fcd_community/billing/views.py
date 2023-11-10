from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
def billing_home(request:HttpRequest):
    return render(request, 'billing/billing_home.html')
