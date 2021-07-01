from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .helpers import * 
from .forms import *
from .models import *
from background_task.models import Task
from .email import *

def index(request):
    return render(request,'writer/index.html')

def pricing(request):
    return render(request,'writer/pricing.html')

@login_required(login_url='login')
def panel(request):
    user=User.objects.get(id=request.user.id)
    # posts = Article.objects.filter(user=user).order_by('-created_on')
    return render(request,'writer/dashboard.html',{'user':user})

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

def login_user(request):
    if request.method== "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/dashboard')
        else:
            messages.info(request,'Invalid credentials. Please try again.')
            return redirect('/login')     
            
    return render(request,"writer/login.html")

def logout_user(request):
    logout(request)
    return redirect("/")

@login_required(login_url='login')
def query(request):
    if request.method == 'POST':
        user=User.objects.get(id=request.user.id)
        query = request.POST.get("query")     
        temperature = float(request.POST.get("customRange"))
        send_email('Temperature: '+str(temperature),query,user.email)
        list_para = get_document(query,user.email,temperature)
        messages.info(request, "Article titled: '{}' is currently being generated. Check your email & dashboard after a few minutes 😃".format(query))  
        return render(request,'writer/dashboard.html')
    else:
        return HttpResponse('Invalid URL')    