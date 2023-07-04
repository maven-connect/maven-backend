from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('joined', views.get_joined_groups, name="joined groups")
]
