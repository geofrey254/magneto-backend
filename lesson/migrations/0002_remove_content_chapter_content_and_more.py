# Generated by Django 5.1.2 on 2024-10-31 10:04

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='chapter_content',
        ),
        migrations.AddField(
            model_name='content',
            name='lesson_content',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]
