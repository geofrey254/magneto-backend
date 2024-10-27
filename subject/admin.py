from django.contrib import admin
from .models import Subject


class subjectAdmin(admin.ModelAdmin):
    list_display = ["title", "image"]


admin.site.register(Subject, subjectAdmin)
