from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from rest_framework.authtoken.models import Token
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth.models import User

@receiver(user_logged_in)
def create_auth_token(sender, request, user, **kwargs):
    token, _ = Token.objects.get_or_create(user=user)
    request.session['auth_token'] = token.key


@receiver(social_account_added)
def save_social_user(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    user_data = sociallogin.account.extra_data
    user.email = user_data.get('email', '')
    user.name = user_data.get('name', '')
    if not user.pk:
        user.save()