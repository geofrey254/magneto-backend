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
    title   = serializers.SerializerMethodField()
    slug    = serializers.SerializerMethodField()  
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ['slug']

    
    def get_title(self, obj):
        return obj.title.title
    
    def get_slug(self, obj):
        return obj.title.title.replace(" ", "-").lower()

