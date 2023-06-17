from django.db import models
from django.contrib.auth import get_user_model

class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(get_user_model())
    batch = models.IntegerField()

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

