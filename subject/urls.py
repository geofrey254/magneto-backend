from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, ClassViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'classes', ClassViewSet, basename='class')

urlpatterns = router.urls