from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    batch = models.IntegerField()

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

