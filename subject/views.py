from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SubjectSerializer, ClassSerializer
from .models import Subject, Classes

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class =  SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer