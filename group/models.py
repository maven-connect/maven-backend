from django.db import models
import uuid
from django.contrib.auth import get_user_model

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(get_user_model(), blank=True)
    batch = models.IntegerField(blank=True, null=True)

    branches = [
        ("CS", "Computer Science"),
        ("ECE", "Electronics"),
        ("MECH", "Mechanical"),
        ("SM", "Smart Manufacturing"),
        ("DS", "Design"),
    ]
    branch = models.CharField(choices=branches, null=True, max_length=4, blank=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    is_BatchCommon = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + ": " + self.content[:10] 

class PermissionIssueMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categories = [
        ("ISS", "Issue"),
        ("PER", "Permission"),
    ]
    category = models.CharField(choices=categories, max_length=3)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category + ": " + self.content[:10] 