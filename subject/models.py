from django.db import models


class Subject(models.Model):
    title = models.CharField(unique=True, null=True, max_length=200)
    image = models.ImageField(upload_to='images/subjects_upload', null=True)
    description = models.CharField(null=True, max_length=800, default="")
    slug = models.SlugField(unique=True, default="", null=True)

    def __str__(self):
        return self.title
