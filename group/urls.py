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
    path('mark-attendance/<str:group_name>/<int:year>/<int:month>/<int:day>/',
         views.mark_attendance, name='mark_group_attendance'),
    path('user-attendance/<int:group_id>/',
         views.user_group_attendance, name="user_attendance_group"),
    path('group-attendance/<int:group_id>/<int:year>/<int:month>/<int:day>/',
         views.users_attended_on_day, name="users_on_day")
]
