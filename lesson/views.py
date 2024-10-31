from django.shortcuts import render
from rest_framework import viewsets
from .serializers import chapterSerializer, contentSerializer
from .models import Chapters, Content


class chapterViewset(viewsets.ModelViewSet):
    queryset = Chapters.objects.all()
    serializer_class = chapterSerializer

class contentViewset(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = contentSerializer