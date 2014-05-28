from OJCR.models import User


class Backend(object):
    
    def authenticate(self, username=None, password=None, **kwargs):

        if not username:
            raise ValueError('Email is not provided for authentication')
        try:
           
            requested_user = User.objects.get(email=username)
            if requested_user.check_password(password):
                return requested_user
            
        except User.DoesNotExist:
            return None
              
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None