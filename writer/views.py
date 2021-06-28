from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .helpers import * 
from .forms import *


def index(request):
    return render(request,'writer/index.html')

def pricing(request):
    return render(request,'writer/pricing.html')

def panel(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        return render(request,'writer/dashboard.html',{'user':user})
    return redirect('/')    

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
    return render(request,'writer/register.html',{'form':form})

def logout_user(request):
    logout(request)
    return redirect("/")

def query(request):
    if request.method == 'POST':
        user=User.objects.get(id=request.user.id)
        query = request.POST.get("query")     
        list_para = get_document(query,user.email)
        messages.info(request, 'Article titled: {} is currently being generated. Check your email & dashboard after a few minutes 😃'.format(query))  
        return render(request,'writer/dashboard.html')
    else:
        return HttpResponse('Invalid URL')    