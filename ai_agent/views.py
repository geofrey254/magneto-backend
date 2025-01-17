from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .agent import run_flow

class MagnetoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        session_data = request.data.get('session_id')  # Extract session data

        # Safely extract the session_id
        session_id = None
        if isinstance(session_data, dict) and 'value' in session_data:
            session_id = session_data['value']  # Use the 'value' key
        elif isinstance(session_data, str):
            session_id = session_data  # Use the string directly

        # Validate inputs
        if not message:
            return Response(
                {"error": "The 'message' field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not session_id:
            return Response(
                {"error": "The 'session_id' field is required and must be valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = run_flow(message, session_id)  # Pass session_id to run_flow
        except Exception as e:
            return Response(
                {"error": f"An error occurred while processing the request: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "prompt": message,
                "magneto": response
            },
            status=status.HTTP_200_OK
        )

