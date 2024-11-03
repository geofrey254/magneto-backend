from rest_framework import serializers
from .models import Chapters, Content
from subject.serializers import SubjectSerializer, ClassSerializer

class chapterSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)  # Nested serializer for Subject model
    form = ClassSerializer(read_only=True) 
    class Meta:
        model = Chapters
        fields = '__all__'
        read_only_fields = ['id']

class contentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ['id']
