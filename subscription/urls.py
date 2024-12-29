from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import subscriptionPlanViewset, subscriptionViewset
from . import views

# Initialize the router and register the viewsets
subs = DefaultRouter()
subs.register(r'subscription_plan', subscriptionPlanViewset, basename='subscription_plan')
subs.register(r'subscription', subscriptionViewset, basename='subscription')

urlpatterns = [
   
    path('mpesa/submit/', views.submit_payment, name='submit_payment'),
    path('mpesa/confirm_payment/', views.confirm_payment, name='confirm_payment'),
]
