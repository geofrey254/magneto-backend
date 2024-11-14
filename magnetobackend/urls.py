from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from subject.urls import router as subject_router
from lesson.urls import lesson as lesson_router
from subscription.urls import subs as subs_router




urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('accounts/', include('allauth.urls')),  # Django allauth endpoints
    path('api/social/login', include('users.urls')), 
    path('api/auth/', include('dj_rest_auth.urls')),  # Login/logout/password management
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration endpoint



    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login (token obtain)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # JWT refresh token

    # Rich text editor (optional)
    path('tinymce/', include('tinymce.urls')),

    # API routes for subjects and lessons
    path('api/', include((subject_router.urls, 'core_api'), namespace='core_api')),
    path('api/', include((lesson_router.urls, 'lesson_api'), namespace='lesson_api')),
    path('api/', include((subs_router.urls, 'subs_api'), namespace='subs_api')),

    # mpesa
    path('', include('subscription.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
