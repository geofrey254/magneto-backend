from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from rest_framework.authtoken.models import Token

@receiver(user_logged_in)
def create_auth_token(sender, request, user, **kwargs):
    token, _ = Token.objects.get_or_create(user=user)
    request.session['auth_token'] = token.key