from django.db import models


class Classes(models.Model):
    name = models.CharField(unique=True, null=True, max_length=10)
    slug = models.SlugField(unique=True, null = True)

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    title = models.CharField(unique=True, null=True, max_length=200)
    image = models.ImageField(upload_to='images/subjects_upload', null=True)
    description = models.CharField(null=True, max_length=800, default="")
    slug = models.SlugField(unique=True, default="", null=True)
    form = models.ManyToManyField(Classes)

    def __str__(self):
        return self.title
