from django_filters import rest_framework as filters
from .models import Content

class ContentFilter(filters.FilterSet):
    slug = filters.CharFilter(method='filter_by_slug')

    def filter_by_slug(self, queryset, name, value):
        # Match the slug generation logic from `get_slug`
        generated_slug = value.replace("-", " ")
        return queryset.filter(title__title__iexact=generated_slug)

    class Meta:
        model = Content
        fields = ['slug']