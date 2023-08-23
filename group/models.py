from django.db import models
import uuid
from django.conf import settings


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    batch = models.IntegerField(blank=True, null=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_groups', null=True)

    branches = [
        ("CS", "Computer Science"),
        ("ECE", "Electronics"),
        ("MECH", "Mechanical"),
        ("SM", "Smart Manufacturing"),
        ("DS", "Design"),
    ]
    branch = models.CharField(
        choices=branches, null=True, max_length=4, blank=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    is_BatchCommon = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + ": " + self.content[:10]


class PermissionIssueMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    categories = [
        ("ISS", "Issue"),
        ("PER", "Permission"),
    ]
    category = models.CharField(choices=categories, max_length=3)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.category + ": " + self.content[:10]


class GroupAttendance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()
    users_attended = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.group.name + " " + str(self.date)
