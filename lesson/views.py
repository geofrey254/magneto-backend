from django.shortcuts import render
from rest_framework import viewsets
from .serializers import chapterSerializer, contentSerializer
from .models import Chapters, Content
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ContentFilter



class chapterViewset(viewsets.ModelViewSet):
    queryset = Chapters.objects.all()
    serializer_class = chapterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']

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