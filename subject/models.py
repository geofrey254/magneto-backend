from django.db import models


class Subject(models.Model):
    title = models.CharField(unique=True, null=True, max_length=200)
    image = models.ImageField(upload_to='images/subjects_upload', null=True)
