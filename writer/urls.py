from django.urls import include,path
from .views import *

urlpatterns = [
    path('query/<str:query>',query_page),
]