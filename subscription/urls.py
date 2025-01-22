from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import subscriptionPlanViewset, subscriptionViewset, paymentHistoryViewset
from . import views

# Initialize the router and register the viewsets
subs = DefaultRouter()
subs.register(r'subscription_plan', subscriptionPlanViewset, basename='subscription_plan')
subs.register(r'subscription', subscriptionViewset, basename='subscription')
subs.register(r'payment_history', views.paymentHistoryViewset, basename='payment_history')

urlpatterns = [
   
    path('submit/<int:plan_id>/', views.submit_payment, name='submit_payment'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
]
