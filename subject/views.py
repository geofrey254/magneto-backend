from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SubjectSerializer, ClassSerializer
from .models import Subject, Classes
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class =  SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']
    pagination_class = None

    # Cache entire viewset
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer
    pagination_class = None

    # Cache entire viewset
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)