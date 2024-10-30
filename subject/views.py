from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SubjectSerializer
from .models import Subject

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class =  SubjectSerializer
