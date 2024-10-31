from rest_framework import serializers
from .models import Subject, Classes

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['title','slug', 'image', 'description', 'form']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['name']
