from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def save_user(request):
    user_data = request.data.get('user', {})
    email = user_data.get('email', '')
    name = user_data.get('name', '')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(email=email, defaults={'username': name})

    if created:
        user.save()
    return Response({'success': 'User created'}, status=status.HTTP_201_CREATED)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        
        user = request.user

        refresh = RefreshToken.for_user(user)
        jwt_access = str(refresh.access_token)
        jwt_refresh = str(refresh)

        frontend_url = "http://localhost:3000"
        query_params = {
            "access": jwt_access,
            "refresh": jwt_refresh,
        }
        redirect_url = f"{frontend_url}?{urlencode(query_params)}"

        return redirect(redirect_url)
