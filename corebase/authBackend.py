from django.contrib.auth.models import User
from institution.models import AuthenticateDataRequest


class DFVABackend(object):

    def authenticate(self, token=None):
        Rauth = AuthenticateDataRequest.objects.filter(
            id_transaction=token).first()
        if Rauth and Rauth.received_notification and Rauth.status == 1:
            try:
                user = User.objects.get(username=Rauth.identification)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=Rauth.identification)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
