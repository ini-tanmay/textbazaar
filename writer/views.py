from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .helpers import * 
from .email import *


def index(request):
    return render(request,'writer/index.html')

def pricing(request):
    return render(request,'writer/pricing.html')

def panel(request):
    return render(request,'writer/dashboard.html')

def create(request):
    return render(request,'writer/create.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/pricing")
    else:
        form = NewUserForm()
    return render(request,'news/register.html',{'form':form})

def logout_user(request):
    logout(request)
    return redirect("/")

def query(request):
    if request.method == 'POST':
        query = request.POST.get("query")     
        list_para = get_document(query,'tanmay.armal@somaiya.edu')
        messages.info(request, 'Article titled: {} is currently being generated. Check your email & dashboard after a few minutes 😃'.format(query))  
        return render(request,'writer/dashboard.html')
    else:
        return HttpResponse('Invalid URL')    