from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
# from background_task.models import Task
from datetime import datetime,timedelta
from .email import *
from .keypoints import *
from django.views.decorators.csrf import csrf_exempt
import razorpay 
from .helpers import *
from .cloud_tasks import send_task
import requests 
import json

@csrf_exempt
def index(request):
    return render(request,'writer/index.html')

def pricing(request):
    return render(request,'writer/pricing.html')

@login_required(login_url='login')
def panel(request):
    user=User.objects.get(id=request.user.id)
    posts = Article.objects.filter(user=user).order_by('-created_on')
    return render(request,'writer/dashboard.html',{'user':user,'post_list':posts})

@login_required(login_url='login')
def plan_payment(request):
    if request.user.is_authenticated:
        return redirect('/pricing#razorpay')
    return redirect('/') 

# @login_required(login_url='login')
# def plan_payment(request):
#     if request.user.is_authenticated:
#         plan=request.GET.get('plan','startup')
#         user=User.objects.get(id=request.user.id)
#         if user.plan==plan:
#            return redirect('/dashboard')
#         amount=159900
#         if plan == 'pro':
#             amount =999900
#         elif plan == 'enterprise':
#             amount = 1999900
#         client = razorpay.Client(auth=('rzp_test_svl7FsV5sWZ9Yc','rX3FSooP6Q7ghiHC0OIv8gWk'))
#         response = client.order.create(dict(amount=amount,currency='INR',notes={
#         "username": request.user.username ,
#         "email": request.user.email ,
#         "id": request.user.id,
#         'purchase':plan 
#         },
#         receipt= str(request.user.id)+'_'+plan+'_'+str(int(datetime.now().timestamp()*1000))+'_'+str(int(amount/100))))
#         print(response)
#         context = {'response':response,'plan':plan}                                                                             
#         return render(request,"writer/payment.html",context)
#     return redirect('/')    


def create(request):
    return render(request,'writer/create.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/dashboard")
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

def create_task(request):
    """ A simple view that triggers the task """
    task = "Example Task"
    send_task(url="/task/", payload=task)
    return HttpResponse('task created')

@login_required(login_url='login')
def query(request):
    title=request.POST.get("query")
    if request.method == 'POST' and title!= None and len(title)>2:
        user=User.objects.get(id=request.user.id)
        if user.credits_bought-user.credits_used==0:
            messages.info(request,"Oops! You're out of credits. Buy a credit pack or upgrade your plan to create more articles. Contact us at letstalk@textbazaar.me for support")  
            return redirect('/dashboard')
        if request.POST.get('keypoints')!=None:
            messages.info(request, "Main keypoints for the article titled: '{}' is currently being generated. Check your email & dashboard after a few seconds 😃".format(title))  
            send_task(url='keypoints/'+query,payload=json.dumps({'userid':user.id}))
            # return get_keypoints(request=request,user=user,title=title).execute()
        temperature = float(request.POST.get("customRange"))
        send_email(title+' is being generated at a Temperature of '+str(temperature),"Article titled: '{}' is currently being generated. Check your email & dashboard after a few seconds 😃".format(title),user.email)
        # get_document(request=request,user=user,title=title,temperature=temperature).execute()
        send_task(url='article/'+query,payload=json.dumps({'temperature':temperature}))
        messages.info(request, "Article titled: '{}' is currently being generated. Check your email & dashboard after a few seconds 😃".format(title))  
        return redirect('/dashboard')
    else:
        return HttpResponse('Invalid Query')    

def get_contents(query):
    url = 'https://us-central1-textbazaar-319010.cloudfunctions.net/get_contents?query={}'.format(query)
    response= requests.post(url)
    data=response.text
    data=json.loads(data)
    return data['contents'],data['videos']

def get_document(request,query):
    payload = request.json()
    print(payload)
    userid=payload.get('userid')
    temperature=payload.get('temperature')
    user=User.objects.get(id=userid)
    contents,videos=get_contents(query)
    contents.sort(key=paragraphs_count)
    url = 'https://us-central1-textbazaar-319010.cloudfunctions.net/get_article?temperature={}'.format(temperature)
    myobj = json.dumps(contents)
    response= requests.post(url, data = myobj)
    if response.ok:
        User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 1)
        try:
            article=Article(user=user,title=query+' at Temperature: '+str(temperature),content=response.text)
            article.save()
        except Exception as e:
            print(e)
            pass
        if videos is not None:
            videos_text='URL: \n\n'.join(videos)
        # images=get_suggested_images(keywords)
        send_email('New Article created at a Temperature of '+str(temperature)+' - '+query, response.text+'/n'+videos_text+'/n', user.email)    
    else: 
        messages.info(request,"Whoops! An error occured while generating the article titled {}. You haven't been charged a Compute Credit. Please Contact us at letstalk@textbazaar.me for support".format(query))  
    return redirect('/dashboard')

def get_keypoints(request,user,query):
    contents,videos=get_contents(query)
    contents.sort(key=paragraphs_count)
    url = 'https://us-central1-textbazaar-319010.cloudfunctions.net/keypoints?no_of_lines=10'
    myobj = json.dumps(contents)
    response= requests.post(url, data = myobj)
    if response.ok:
        User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 1)
        try:
            article=Article(user=user,title='KeyPoints: '+query,content=response.text)
            article.save()
        except Exception as e:
            print(e)
            pass
        send_email('New Keypoints List created: '+query, response.text, user.email)    
    else:     
        messages.info(request,"Whoops! Something went wrong on our end. You haven't been charged a Compute Credit. Please Contact us at letstalk@textbazaar.me for support")  
    return redirect('/dashboard')