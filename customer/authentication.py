from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomUser = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        try:
            # Allow login with either email or username
            if email:
                user = CustomUser.objects.get(email=email)
            elif username:
                user = CustomUser.objects.get(username=username)
            else:
                return None
            if user.check_password(password):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None