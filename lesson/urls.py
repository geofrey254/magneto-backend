from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import chapterViewset, contentViewset

lesson = DefaultRouter()
lesson.register(r'chapters', chapterViewset, basename='chapter')
lesson.register(r'content', contentViewset, basename='content')

urlpatterns = lesson.urls