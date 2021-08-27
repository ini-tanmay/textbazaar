"""TextBazaar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django_cloud_tasks import urls as dct_urls
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from writer.shopify_helpers import *
from writer.mytts import tts
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('writer.urls')),
    path('blog/', include('blog.urls')),
    re_path('djga/', include('google_analytics.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('uploads/favicon.ico'))),
    path("password-reset", auth_views.PasswordResetView.as_view( template_name="writer/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view( template_name="writer/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="writer/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="writer/password_reset_complete.html"), name="password_reset_complete"),
    path('shopify/login',shop_login),
    path('shopify/login/finalize',get_token),
    path('shopify/buy/<str:plan_type>',buy_plan),
    path('shopify/buy/credits/<str:plan_type>',buy_credits),
    path('shopify/buy/confirm/plan/<str:plan_type>',confirm_purchase_plan),
    path('shopify/buy/confirm/credits',confirm_purchase_credits),
    path('customers/data_request',customers_data_request),
    path('customers/redact',customers_redact),
    path('shop/redact', shop_redact),
    path('tts', tts),
    # path('shopify/test',test),
    
    # path('_tasks/', include(dct_urls)),
]
