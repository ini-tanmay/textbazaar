import shopify
import os
import binascii
from django.shortcuts import redirect


shopify.Session.setup(api_key='d9d3a4134fbb7592a9846f07df45a071', secret='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')
shop_url = "textbazaar.myshopify.com"
api_version = '2021-04'

def shop_login(request):
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = "https://textbazaar.me/shopify/login/finalize"
    scopes = ['read_products', 'read_orders']
    newSession = shopify.Session(shop_url, api_version)
    auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
    return redirect(auth_url)

def get_token(request):
    session = shopify.Session(shop_url, api_version)
    access_token = session.request_token(request.GET) # request_token will validate hmac and timing attacks
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session) 

def buy(request):
    application_charge = shopify.ApplicationCharge.create({
    'name': 'Subscription',
    'price': 1234.00,
    'test': True,
    'return_url': 'https://textbazaar.me/blog'
    })
    return redirect(application_charge.confirmation_url)
