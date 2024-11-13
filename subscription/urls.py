from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import subscriptionPlanViewset, subscriptionViewset

subs = DefaultRouter()
subs.register(r'subscription_plan', subscriptionPlanViewset, basename='subscription plan')
subs.register(r'subscription', subscriptionViewset, basename='subscription')

urlpatterns = subs.urls