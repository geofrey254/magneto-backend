# Generated by Django 5.1.2 on 2024-12-30 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_subscriptionplan_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='ref',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
