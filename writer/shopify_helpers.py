import shopify
import os
import binascii
from django.shortcuts import redirect

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
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    return redirect('/') 

def buy_plan(request,plan_type):
    price=200.00
    if 'pro' in plan_type:
        price=400.00
    elif 'enterprise' in plan_type:
        price=6,687.00    
    application_charge = shopify.RecurringApplicationCharge.create({
    'name': plan_type.upper(),
    'price': price,
    'test': True,
    'return_url': 'https://textbazaar.me/shopify/buy/confirm'
    })
    return redirect(application_charge.confirmation_url)

def confirm_purchase(request):
    print(request.GET)
    pass
