from django.db import models  
from subject.models import Classes, Subject 
from tinymce.models import HTMLField


class Chapters(models.Model):
    title = models.CharField(null=True, unique=True, max_length=100)    
    description = models.CharField(null=True, unique=True, max_length=250)
    # Foreign key to the Subject model, allows for linking chapters to a specific subject
    # If the subject is deleted, set this field to NULL
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    # Foreign key to the Classes model, allowing chapters to be linked to a specific class
    # If the class is deleted, set this field to NULL
    form = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.subject.title if self.subject else 'No Subject'} - {self.form.name if self.form else 'No Class'}"


# Content model representing the content of the chapters
class Content(models.Model):
    # One-to-one relationship with Chapters, meaning each chapter can have one corresponding content entry
    # If the chapter is deleted, delete this content as well
    title = models.OneToOneField(Chapters, on_delete=models.CASCADE, primary_key=True)
    lesson_content = HTMLField(null=True)

    def __str__(self):
        return f"Content for {self.title.title}"
