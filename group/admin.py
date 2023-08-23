from django.contrib import admin

from .models import Group, Message, PermissionIssueMessage

admin.site.register(Group)
admin.site.register(Message)
admin.site.register(PermissionIssueMessage)
