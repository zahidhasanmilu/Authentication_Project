from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackEnd(ModelBackend):
    def authenticate(self,  username=None, password=None, **kwargs):
        CustomUser = get_user_model()
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    
