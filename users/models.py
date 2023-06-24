from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    batch = models.IntegerField(null=True, blank=True)
    
    branches = [
        ("CS", "Computer Science"),
        ("ECE", "Electronics"),
        ("MECH", "Mechanical"),
        ("SM", "Smart Manufacturing"),
        ("DS", "Design"),
    ]
    branch = models.CharField(choices=branches, null=True, max_length=4, blank=True)
