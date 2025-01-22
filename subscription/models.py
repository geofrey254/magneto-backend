# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now

from .paystack import Paystack

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(null=True)
    amount = models.IntegerField(null=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name     

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)


    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = now()

        if self.verified:
            existing_subscription = Subscription.objects.filter(user=self.user, plan=self.plan, verified=True).first()  

            if existing_subscription:
                return

      
        if self.plan.duration:
            self.end_date = self.start_date + timedelta(days=self.plan.duration)
        else:
          
            raise ValueError("The plan duration must be set and cannot be None or 0.")
        
        super().save(*args, **kwargs)

    def is_active(self):
        if not self.verified:
            return False
        return self.end_date > now()
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.start_date} to {self.end_date}"
    
    def check_and_update_verification(self):
        """Check if the subscription has expired, and set verified to False if so."""
        if self.end_date and self.end_date <= now():
            if self.verified:
                self.verified = False
                self.save()
                print(f"Subscription for {self.user.username} has expired and is now marked as unverified.")
        else:
            print(f"Subscription for {self.user.username} is still active.")


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    reference_code = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_paid} - {self.reference_code}"