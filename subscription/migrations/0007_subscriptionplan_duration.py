# Generated by Django 5.1.2 on 2024-12-31 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0006_alter_subscriptionplan_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]