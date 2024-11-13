from django.shortcuts import render
from rest_framework import viewsets
from .serializers import subscriptionPlanSerializer, subscriptionSerializer
from .models import Subscription, SubscriptionPlan
from django_filters.rest_framework import DjangoFilterBackend



class subscriptionPlanViewset(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = subscriptionPlanSerializer
    filter_backends = [DjangoFilterBackend]

class subscriptionViewset(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = subscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'plan'