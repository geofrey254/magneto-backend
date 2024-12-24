# views.py

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urljoin, urlencode
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import redirect



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        if response.status_code != 200:
            return Response({"error": "Failed to exchange code for tokens"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract tokens from the response
        tokens = response.json()
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        if not access_token or not refresh_token:
            return Response({"error": "Failed to retrieve tokens"}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the frontend redirect URL
        frontend_url = "http://localhost:3000"  # Update with your actual frontend domain in production
        query_params = {
            "access": access_token,
            "refresh": refresh_token,
        }
        redirect_url = f"{frontend_url}?{urlencode(query_params)}"

        # Redirect the user to the frontend with tokens in the query parameters
        return redirect(redirect_url)
