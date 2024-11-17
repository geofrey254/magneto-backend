from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from . import views
from .views import GoogleLogin, GoogleLoginCallback



urlpatterns = [
    # URLs will come here
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path(
        "dj-rest-auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
]