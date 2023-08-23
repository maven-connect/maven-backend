from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('joined', views.get_joined_groups, name="joined groups"),
    path('<str:group>/data', views.get_group_data, name="group data"),
    path('<str:group_name>/participants',
         views.get_group_participants, name="group participants"),
    path('new', views.new_group, name="new group"),
    path('<str:group_name>/approve', views.approve_PermIssue,
         name="approve permission issue"),
]
