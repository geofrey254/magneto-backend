from django.contrib import admin
from .models import Subject, Classes


class subjectAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ["title"]}

class classAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}



admin.site.register(Subject, subjectAdmin)
admin.site.register(Classes, classAdmin)
