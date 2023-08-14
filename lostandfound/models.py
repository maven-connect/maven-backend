from django.db import models
import uuid
from django.conf import settings


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class LostAndFoundModel(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    creator = models.ManyToManyField(settings.AUTH_USER_MODEL)
    categories = [
        ("LOST", "Lost"),
        ("FOUND", "Found"),
    ]
    category = models.CharField(
        choices=categories, max_length=5, null=False, blank=False)

    def __str__(self):
        return self.name
