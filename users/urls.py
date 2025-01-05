from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from . import views
from .views import GoogleLoginVerifyView



urlpatterns = [
    # URLs will come here
    path('google/login/', GoogleLoginVerifyView.as_view(), name='google_login'),
]