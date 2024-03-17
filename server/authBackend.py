from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class CustomAuth(BaseBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        if password is None:
            try:
                user = UserModel.objects.get(email=email)
                return user
            except UserModel.DoesNotExist:
                return None
        else:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return None
            else:
                print(user.password, user.check_password(password), password)
                if user.password == password or user.check_password(password):
                    return user
                else:
                    return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
