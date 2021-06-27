from django.urls import include,path
from .views import *

urlpatterns = [
    path('',index),
    path('query/<str:query>/<str:email>',query_page),
]