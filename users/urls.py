from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from . import views
from .views import GoogleLogin, GoogleLoginCallback



urlpatterns = [
    # URLs will come here
   
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path(
        "google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_callback",
    ),
]