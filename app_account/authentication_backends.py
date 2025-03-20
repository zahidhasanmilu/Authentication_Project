from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # Use email as the username for authentication
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
