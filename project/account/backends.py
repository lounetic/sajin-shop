from django.contrib.auth.backends import ModelBackend

from .models import User


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = kwargs.get('phone')
        if phone is None or password is None:
            return
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user