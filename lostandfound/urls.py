from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('create', views.createLostFound,
         name="create lost and found"),
    path('all', views.getLostFoundItems, name='Get lost found items')
]
