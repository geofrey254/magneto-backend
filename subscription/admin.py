from django.contrib import admin
from .models import SubscriptionPlan, Subscription, PaymentHistory

# Register your models here.
@admin.register(SubscriptionPlan)
class subscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Subscription)
class subscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "plan"]

@admin.register(PaymentHistory)
class paymentHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "amount_paid", "reference_code"]