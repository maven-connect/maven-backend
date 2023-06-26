from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class googleAuthBackend(BaseBackend):

    def authenticate(self, request, email=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

class EmailPasswordBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email, password=password)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        print(user_id, 'email')

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None