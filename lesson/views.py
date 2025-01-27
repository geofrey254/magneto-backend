from django.shortcuts import render
from rest_framework import viewsets
from .serializers import chapterSerializer, contentSerializer
from .models import Chapters, Content
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ContentFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.files.storage import default_storage
from django.http import JsonResponse
import os
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class chapterViewset(viewsets.ModelViewSet):
    queryset = Chapters.objects.all()
    serializer_class = chapterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']

    @method_decorator(cache_page(60 * 15))  # Cache list action
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # Cache retrieve action
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_slug = self.request.query_params.get('subject')
        if subject_slug:
            queryset = queryset.filter(subject__slug=subject_slug)
        return queryset

class contentViewset(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = contentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContentFilter
    lookup_field = 'title__slug'

    @method_decorator(cache_page(60 * 15))  # Cache list action
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # Cache retrieve action
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
@csrf_exempt
def tinymce_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']
            # Generate unique filename to avoid overwrites
            filename = default_storage.get_valid_name(uploaded_file.name)
            file_path = os.path.join('tinymce_uploads', filename)
            saved_path = default_storage.save(file_path, uploaded_file)
            
            # Construct URL using MEDIA_URL (avoids hardcoding)
            file_url = default_storage.url(saved_path)
            absolute_url = request.build_absolute_uri(file_url)
            
            return JsonResponse({'location': absolute_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No file provided'}, status=400)
