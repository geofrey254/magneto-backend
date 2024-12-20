from django.urls import path
from .views import MagnetoAPIView

urlpatterns = [
    path('magneto_agent/', MagnetoAPIView.as_view(), name='message-api'),
]