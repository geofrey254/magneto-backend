# Generated by Django 5.1.2 on 2024-10-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, null=True, unique=True)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='form',
            field=models.ManyToManyField(to='subject.classes'),
        ),
    ]
