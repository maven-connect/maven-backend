from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db import models  
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone  
from django.utils.translation import gettext_lazy as _  
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):  
    username = None  
    email = models.EmailField(_('email_address'), unique=True, max_length = 200)  
    date_joined = models.DateTimeField(default=timezone.now)  
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  
    is_verified = models.BooleanField(default=False)
    batch = models.IntegerField(null=True, blank=True)
    branches = [
        ("CS", "Computer Science"),
        ("ECE", "Electronics"),
        ("MECH", "Mechanical"),
        ("SM", "Smart Manufacturing"),
        ("DS", "Design"),
    ]
    user_branch = models.CharField(choices=branches, null=True, max_length=4, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):  
        return True  
  
    def is_staff(self):  
         return self.staff  
    
    @property  
    def is_admin(self):  
        return self.admin  
  
    def __str__(self):  
        return self.email  
