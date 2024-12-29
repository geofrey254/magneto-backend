# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from .paystack import Paystack

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    amount = models.IntegerField(null=True)
    verified = models.BooleanField(default=False)
    ref = models.CharField(max_length=20, unique=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name == 'daily':
            self.amount = 30
        elif self.name == 'monthly':
            self.amount = 700
        elif self.name == 'yearly':
            self.amount = 7400
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    class Meta:
        ordering = ['-start_date']

    def is_active(self):
        return self.end_date > timezone.now()
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.start_date} to {self.end_date}"
