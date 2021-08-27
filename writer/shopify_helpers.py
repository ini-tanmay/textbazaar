from django.http.response import HttpResponse
import shopify
import os
import binascii
from django.shortcuts import redirect
from .models import User
from django.contrib.auth import login
from django.db.models import F
from .email import send_email
shopify.Session.setup(api_key='d9d3a4134fbb7592a9846f07df45a071', secret='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')
api_version = '2021-04'

def shop_login(request):
    shop_url=request.GET.get('shop')
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = "https://textbazaar.me/shopify/login/finalize"
    scopes = ['read_products']
    newSession = shopify.Session(shop_url, api_version)
    auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
    return redirect(auth_url)

def get_token(request):
    shop_url=request.GET.get('shop')
    session = shopify.Session(shop_url, api_version)
    access_token = session.request_token(request.GET) # request_token will validate hmac and timing attacks
    user=User(username=shop_url.split('.')[0],first_name=shop_url.split('.')[0],shop_url=shop_url,access_token=access_token,password=shop_url)
    user.save()
    login(request, user)
    shopify.ShopifyResource.activate_session(session)
    try:
        send_email('New user joined','check textbazaar '+str(shop_url), 'tanmay.armal@somaiya.edu')    
    except:
        pass    
    return redirect('/') 

def buy_plan(request,plan_type):
    price=100.00
    if 'pro' in plan_type:
        price=175.00
    elif 'enterprise' in plan_type:
        price=13430.00    
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)
    subscription = shopify.RecurringApplicationCharge.create({
    'name': plan_type.upper(),
    'price': price,
    'test': False,
    'return_url': 'https://textbazaar.me/shopify/buy/confirm/plan/'+plan_type
    })
    return redirect(subscription.confirmation_url)

def buy_credits(request,plan_type):
    price=245
    if 'pro' in plan_type:
        price=250
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)
    application_charge = shopify.ApplicationCharge.create({
    'name': plan_type.upper() +': 20 Compute Credits',
    'price': price,
    'test': False,
    'return_url': 'https://textbazaar.me/shopify/buy/confirm/credits'
    })
    return redirect(application_charge.confirmation_url)

def confirm_purchase_plan(request,plan_type):
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)
    charge_id=request.GET.get('charge_id')
    activated_charge = shopify.RecurringApplicationCharge.find(charge_id)
    is_paid ='active' in activated_charge.status 
    if is_paid:
        if user.is_paid:
            user.credits_bought=0
        initial_credits=user.credits_bought    
        if 'pro' in plan_type:
            user.credits_bought=initial_credits+45
        elif 'startup' in plan_type:
            user.credits_bought=initial_credits+25
        elif 'enterprise' in plan_type:
            user.credits_bought=initial_credits+1000
        user.plan=plan_type
        user.is_paid=True
        user.plan_order_id=charge_id
        user.save()
    return redirect('/dashboard')

def confirm_purchase_credits(request):
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)
    charge_id=request.GET.get('charge_id')
    activated_charge = shopify.ApplicationCharge.find(charge_id)
    is_paid ='active' in activated_charge.status 
    if is_paid:
        initial_credits=user.credits_bought    
        user.credits_bought=initial_credits+20
        user.credit_order_id=charge_id
        user.save()
    return redirect('/dashboard')

def customers_data_request(request):
    return HttpResponse('No Data')

def customers_redact(request):
    return HttpResponse('No Data')

def shop_redact(request):
    shop_id=request.POST.get('shop_id')
    shop_domain=request.POST.get('shop_domain')
    try:
        send_email('Deletion request',shop_id+shop_domain,'tanmay.armal@somaiya.edu')
    except:
        pass    
    return HttpResponse('The data will be deleted within 48hours.')


# def test(request):
#     user=User.objects.get(id=request.user.id)    
#     session = shopify.Session(user.shop_url, api_version, user.access_token)
#     shopify.ShopifyResource.activate_session(session)
#     shop=shopify.User()
#     print(shop.name)
#     print(shop.email)
    