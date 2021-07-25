from django.urls import include,path
from .views import *
from .shopify_helpers import shop_login,get_token, buy_plan,confirm_purchase
urlpatterns = [
    # path('django_plotly_dash/', include('django_plotly_dash.urls')),
    # path('credits_payment',credits_payment),
    # path('success',payment_success,name='success'),
    path('',index),
    path('shopify/login',shop_login),
    path('shopify/login/finalize',get_token),
    path('shopify/buy/<str:plan_type>',buy_plan),
    path('shopify/buy/confirm',confirm_purchase),
    path('ref/<str:code>',referral),
    path('pricing',pricing),
    path('dashboard',panel),
    path('create',create),
    path('payment',plan_payment),
    path('signup',register),
    path('logout',logout_user),
    path('login',login_user,name='login'),
    path('query',query),
    path('keypoints/',get_keypoints),
    path('article/',get_document),
    path('affiliate',affiliate),
]