from django.contrib import admin
from .models import Chapters, Content

# Register your models here.
@admin.register(Chapters)
class chapterAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "form"]
    prepopulated_fields = {"slug" : ["title"]}



@admin.register(Content)
class contentAdmin(admin.ModelAdmin):
    list_display = ["title"]
    




