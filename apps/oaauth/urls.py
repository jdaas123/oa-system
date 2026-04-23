from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'oaauth'

urlpatterns = [
    path('login',LoginView.as_view(),name = 'login'),
    path('resetpwd',ResetPwdView.as_view(),name = 'resetpwd'),
]