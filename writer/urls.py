from django.urls import include,path
from .views import *

urlpatterns = [
    path('',index),
    path('pricing',pricing),
    path('dashboard',panel),
    path('create',create),
    path('payment',plan_payment),
    # path('django_plotly_dash/', include('django_plotly_dash.urls')),
    # path('credits_payment',credits_payment),
    # path('success',payment_success,name='success'),
    path('signup',register),
    path('logout',logout_user),
    path('login',login_user,name='login'),
    path('query',query),
    path('keypoints/<str:query>',get_keypoints),
]