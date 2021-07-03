from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from background_task.models import Task
from datetime import datetime,timedelta
from .email import *
from .keypoints import *
from django.views.decorators.csrf import csrf_exempt
import razorpay 

@csrf_exempt
def index(request):
    return render(request,'writer/index.html')

def pricing(request):
    return render(request,'writer/pricing.html')

@login_required(login_url='login')
def panel(request):
    user=User.objects.get(id=request.user.id)
    # posts = Article.objects.filter(user=user).order_by('-created_on')
    return render(request,'writer/dashboard.html',{'user':user})

@login_required(login_url='login')
def plan_payment(request):
    if request.user.is_authenticated:
        plan=request.GET.get('plan','startup')
        user=User.objects.get(id=request.user.id)
        if user.plan==plan:
           return redirect('/dashboard')
        amount=159900
        if plan == 'pro':
            amount =999900
        elif plan == 'enterprise':
            amount = 1999900
        client = razorpay.Client(auth=('rzp_test_svl7FsV5sWZ9Yc','rX3FSooP6Q7ghiHC0OIv8gWk'))
        response = client.order.create(dict(amount=amount,currency='INR',notes={
        "username": request.user.username ,
        "email": request.user.email ,
        "id": request.user.id,
        'purchase':plan 
        },
        receipt= str(request.user.id)+'_'+plan+'_'+str(int(datetime.now().timestamp()*1000))+'_'+str(int(amount/100))))
        print(response)
        context = {'response':response,'plan':plan}                                                                             
        return render(request,"writer/payment.html",context)
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
    title=request.POST.get("query")
    if request.method == 'POST' and title!= None and len(title)>2:
        user=User.objects.get(id=request.user.id)
        if request.POST.get('keypoints')!=None:
            messages.info(request, "Main keypoints for the article titled: '{}' is currently being generated. Check your email & dashboard after a few minutes 😃".format(title))  
            return get_keypoints(request,title)
        temperature = float(request.POST.get("customRange"))
        send_email('Temperature: '+str(temperature),title,user.email)
        list_para = get_document(title,user.email,temperature)
        messages.info(request, "Article titled: '{}' is currently being generated. Check your email & dashboard after a few minutes 😃".format(title))  
        return render(request,'writer/dashboard.html')
    else:
        return HttpResponse('Invalid URL')    

def get_keypoints(request,query):
    value=summarize(contents)
    return render(request,'writer/dashboard.html')   