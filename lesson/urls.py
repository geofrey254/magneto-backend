from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import chapterViewset, contentViewset, tinymce_upload

# Create a router and register your viewsets
lesson = DefaultRouter()
lesson.register(r'chapters', chapterViewset, basename='chapter')
lesson.register(r'content', contentViewset, basename='content')

# Define your URL patterns
urlpatterns = [
    # Include the router's URLs
    path('', include(lesson.urls)),

    # Add the custom URL for TinyMCE file upload
    path('tinymce/upload/', tinymce_upload, name='tinymce_upload'),
]