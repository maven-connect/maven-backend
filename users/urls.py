from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('google-login', views.googleLogin, name="googleLogin"),
    path('login', views.login_view, name="login"),
    path('logout', views.login_view, name="logout"),
    path('register-user', views.register_user, name="register user"),
    path('verify-user', views.verify_user, name="verify user"),
    path('', views.home, name="home")
]
