from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .agent import run_flow

class MagnetoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        message = request.data.get('message', "")
        response = run_flow(message)

        return Response(
            {
                "prompt":message,
                "magneto":response
            }, status=status.HTTP_200_OK
        )
