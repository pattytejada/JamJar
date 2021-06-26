from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    """Home page output when taking in request"""
    return render(request, 'blog/home.html')
