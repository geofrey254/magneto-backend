from rest_framework import serializers
from .models import Subject, Classes

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'name']

class SubjectSerializer(serializers.ModelSerializer):
    form = ClassSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'image', 'description', 'form']
