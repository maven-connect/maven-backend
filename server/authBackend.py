from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class googleAuthBackend(ModelBackend):

    def authenticate(self, request, email=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=email)
            return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

class EmailPasswordBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None