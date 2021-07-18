from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .cloud_tasks import send_task
from .forms import *
from .models import User,Article
from datetime import datetime,timedelta
from .email import *
from .keypoints import *
from django.views.decorators.csrf import csrf_exempt
from .helpers import *
import requests 
import json
import re
from .testimonials import testimonials

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    data=[]
    for i in range(len(testimonials)):
        img_url="../static/uploads/comment_bg{}.jpg".format(i+2)
        testimonials[i].img=img_url
        testimonials[i].div="pt-75 pb-75 testimonial_{}".format(i+1)
        data.append(testimonials[i])
    return render(request,'writer/index.html',{'data':data})

def pricing(request):
    return render(request,'writer/pricing.html')

def affiliate(request):
    return render(request,'writer/affiliate.html')

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
    results=get_cloud_languages()
    return render(request,'writer/create.html',context={'languages':results})

def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            send_email('New user joined','check textbazaar', 'tanmay.armal@somaiya.edu')    
            user = form.save()
            login(request, user)
            return redirect("/dashboard")
    else:
        form = NewUserForm()
        if mobile(request):
            return render(request,'writer/register.html',{'form':form})
        else:
            return render(request,'writer/signup.html',{'form':form})    

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
    return render(request,'writer/login_pc.html')            

def logout_user(request):
    logout(request)
    return redirect("/")


@login_required(login_url='login')
def query(request):
    title=request.POST.get("query")
    if "Don't translate" in request.POST.get('translate'):
        translate='en'
    else: 
        translate=request.POST.get('translate').split(' ')[-1]
    print(translate)    
    if request.method == 'POST' and title!= None and len(title)>2:
        user=User.objects.get(id=request.user.id)
        if user.credits_bought-user.credits_used<=0:
            messages.info(request,"Oops! You're out of credits. Buy a credit pack or upgrade your plan to create more articles. Contact us at letstalk@textbazaar.me for support")  
            return redirect('/dashboard')
        if request.POST.get('keypoints')!=None:
            # get_keypoints(request,user,title)
            send_task(url='/keypoints/',payload=json.dumps({'userid':user.id,'query':title,'translate':translate}))
            messages.info(request, "Main keypoints for the article titled: '{}' is currently being generated. Check your email & dashboard after a few minutes 😃".format(title))  
            return redirect('/dashboard')
        else:
            temperature = float(request.POST.get("customRange"))
            # send_email(title+' is being generated at a Temperature of '+str(temperature),"Article titled: '{}' is currently being generated. Check your email & dashboard after a few minutes 😃".format(title),user.email)
            # get_document(request,user,title,temperature)
            if "Don't translate" in request.POST.get('translate'):
                translate='en'
            send_task(url='/article/',payload=json.dumps({'userid':user.id,'temperature':temperature,'query':title,'translate':translate}))
            messages.info(request, "Article titled: '{}' is currently being generated. Check your email & dashboard after a few minutes 😃".format(title))  
        return redirect('/dashboard')
    else:
        return HttpResponse('Invalid Query')    

def get_contents(query):
    url = 'https://us-central1-textbazaar-319010.cloudfunctions.net/get_contents?query={}'.format(query)
    response= requests.post(url)
    data=response.text
    data=json.loads(data)
    return data['contents'],data['videos']
    
@csrf_exempt
def get_document(request):
    payload = json.loads(request.body.decode('utf-8'))
    print(payload)
    userid=payload.get('userid')
    query=payload.get('query')
    temperature=payload.get('temperature')
    user=User.objects.get(id=userid)
    print('Article started by: '+user.email)
    contents,videos=get_contents(query)
    contents.sort(key=paragraphs_count)
    url = 'https://us-central1-textbazaar-319010.cloudfunctions.net/get_article?temperature={}'.format(temperature)
    myobj = json.dumps(contents)
    response= requests.post(url, data = myobj)
    translated=paraphrase(response.text,payload.get('translate'))
    translated=translated.replace('&#39;',"'")
    translated=translated.replace('&quot;','"')
    videos_text=''
    if response.ok:
        if videos is not None:
            videos_text= '\r\r\nRelevant Videos: \r\r\n'+'URL: \n\n'.join(videos)
        if 'en' not in payload.get('translate'):
            User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 2)
        else:
            User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 1)
        try:
            article=Article(user=user,title=query+' at Temperature: '+str(temperature),content=translated+videos_text)
            article.save()
        except Exception as e:
            print(e)
            pass
        # images=get_suggested_images(keywords)
        send_email('New Article created at a Temperature of '+str(temperature)+' - '+query, translated+videos_text, user.email)    
    else: 
        messages.info(request,"Whoops! An error occured while generating the article titled {}. Please Contact us at letstalk@textbazaar.me for support".format(query))  
    return HttpResponse('done')

@csrf_exempt
def get_keypoints(request):
    payload = json.loads(request.body.decode('utf-8'))
    print(payload)
    userid=payload.get('userid')
    query=payload.get('query')
    user=User.objects.get(id=userid)
    print('Keypoints started by: '+user.email)
    contents,videos=get_contents(query)
    contents.sort(key=paragraphs_count)
    lines=10
    if user.plan=='pro':
        lines=30
    if user.plan=='enterprise':
        lines=50
    url = 'https://us-central1-textbazaar-319010.cloudfunctions.net/keypoints?no_of_lines='+str(lines)
    myobj = json.dumps(contents)
    response= requests.post(url, data = myobj)
    translated=paraphrase(response.text,payload.get('translate'))
    translated=translated.replace('&#39;',"'")
    translated=translated.replace('&quot;','"')
    if response.ok:
        if 'en' not in payload.get('translate'):
            User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 2)
        else:
            User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 1)
        try:
            article=Article(user=user,title='KeyPoints: '+query,content=translated)
            article.save()
        except Exception as e:
            print(e)
            pass
        translated=translated.replace('.','\r\r\n')
        send_email('New Keypoints List created: '+query, translated, user.email)    
    else:     
        messages.info(request,"Whoops! Something went wrong on our end. Please Contact us at letstalk@textbazaar.me for support")  
    return HttpResponse('done')
