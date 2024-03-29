from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create a superuser with administrative privileges
        superuser = self.create_user(email, password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_userStaff = True
        superuser.save()
        return superuser
