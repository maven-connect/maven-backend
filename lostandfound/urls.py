from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('create', views.createLostFound,
         name="create lost found item"),
    path('all', views.getLostFoundItems, name='Get lost found items'),
    path('delete', views.deleteLostFoundItem, name="delete lost found item")
]
