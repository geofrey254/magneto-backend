from django.shortcuts import redirect
from django.conf import settings
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount import providers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.socialaccount.helpers import complete_social_login

class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]  # If you want the callback to be publicly accessible
    
    def get(self, request, *args, **kwargs):
        # Get the code from the URL parameters (not the body)
        code = request.GET.get('code')

        if code:
            try:
                # Use the Google OAuth2 adapter to complete the login
                adapter = GoogleOAuth2Adapter()
                # Call the `complete_login` method using the code received from Google
                login = adapter.complete_login(request, code)
                # Use the helper function to complete the login
                complete_social_login(request, login)

                # Return a success response with a token or other info
                return Response({'token': login.token.key}, status=200)
            except Exception as e:
                # If there's an error completing the login, return an error response
                return Response({'error': str(e)}, status=400)

        # If the code wasn't provided, return an error
        return Response({'error': 'Invalid code'}, status=400)
