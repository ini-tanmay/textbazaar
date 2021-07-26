import shopify
import os
import binascii
from django.shortcuts import redirect
from .models import User
from django.contrib.auth import login
from django.db.models import F

shopify.Session.setup(api_key='d9d3a4134fbb7592a9846f07df45a071', secret='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')
api_version = '2021-04'

def shop_login(request):
    shop_url=request.GET.get('shop')
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = "https://textbazaar.me/shopify/login/finalize"
    scopes = ['read_products', 'read_orders']
    newSession = shopify.Session(shop_url, api_version)
    auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
    return redirect(auth_url)

def get_token(request):
    print(request.GET)
    shop_url=request.GET.get('shop')
    session = shopify.Session(shop_url, api_version)
    access_token = session.request_token(request.GET) # request_token will validate hmac and timing attacks
    user=User(username=shop_url.split('.')[0],first_name=shop_url.split('.')[0],shop_url=shop_url,access_token=access_token)
    user.save()
    login(request, user)
    shopify.ShopifyResource.activate_session(session)
    return redirect('/') 

def buy_plan(request,plan_type):
    print(type(plan_type))
    price=100.00
    if 'pro' in plan_type:
        price=175.00
    elif 'enterprise' in plan_type:
        price=13,430.00    
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)
    subscription = shopify.RecurringApplicationCharge.create({
    'name': plan_type.upper(),
    'price': price,
    'test': True,
    'return_url': 'https://textbazaar.me/shopify/buy/confirm'
    })
    return redirect(subscription.confirmation_url)

def buy_credits(request,plan_type):
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)
    application_charge = shopify.ApplicationCharge.create({
    'name': plan_type.upper() +': 20 credits',
    'price': 249.00,
    'test': True,
    'return_url': 'https://textbazaar.me/shopify/buy/confirm'
    })
    return redirect(application_charge.confirmation_url)

def confirm_plan_purchase(request):
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)

    charge_id=request.GET.get('charge_id')
    shopify.ApplicationCharge.activate(charge_id)
    activated_charge = shopify.ApplicationCharge.find(charge_id)
    user.is_paid = activated_charge.status == 'active'
    return redirect('/dashboard')

def confirm_plan_credits(request):
    user=User.objects.get(id=request.user.id)    
    session = shopify.Session(user.shop_url, api_version, user.access_token)
    shopify.ShopifyResource.activate_session(session)

    charge_id=request.GET.get('charge_id')
    shopify.ApplicationCharge.activate(charge_id)
    activated_charge = shopify.ApplicationCharge.find(charge_id)
    is_paid = activated_charge.status == 'active'
    if is_paid:
        User.objects.filter(id = user.id).update(credits_used=F('credits_used') + 20)
        user.is_paid=True
        user.save()
    return redirect('/dashboard')
