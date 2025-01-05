from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class GoogleLoginVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_token_str = request.data.get('id_token')

        if not id_token_str:
            return Response({"error": "No ID token provided."}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request())

            # Get user information
            email = idinfo['email']
            user, _ = User.objects.get_or_create(username=email, email=email)

            # Generate JWT for the user
            refresh = RefreshToken.for_user(user)
            print(refresh)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        except ValueError:
            return Response({"error": "Invalid token."}, status=400)
