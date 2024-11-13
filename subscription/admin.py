from django.contrib import admin
from .models import SubscriptionPlan, Subscription

# Register your models here.
@admin.register(SubscriptionPlan)
class subscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Subscription)
class subscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "plan"]