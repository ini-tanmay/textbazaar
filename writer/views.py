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



def query_page(request,query,email):
    list_para = get_document(query,email)
    return render(request,'writer/results.html',{'final':'Thanks! Your blog article will be emailed to you within 50 seconds'})