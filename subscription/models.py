# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date > timezone.now()
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.start_date} to {self.end_date}"
