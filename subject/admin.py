from django.contrib import admin
from .models import Subject


class subjectAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Subject, subjectAdmin)
