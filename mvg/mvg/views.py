from django.http import HttpResponse
from django.shortcuts import render

def homepage(request, *args, **kwargs):
    return render(request,"homepage.html")

