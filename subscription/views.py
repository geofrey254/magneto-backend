import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import subscriptionPlanSerializer, subscriptionSerializer
from .models import Subscription, SubscriptionPlan
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import requests

class subscriptionPlanViewset(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = subscriptionPlanSerializer
    filter_backends = [DjangoFilterBackend]

class subscriptionViewset(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = subscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'plan'


@csrf_exempt
def submit_payment(request):
     if request.method == "POST":
        data = json.loads(request.body)
        amount = int(data.get("amount")) * 100
        email = data.get("email")
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": email,
            "amount": amount,
            "callback_url": "http://localhost:3000/subscription/success",
        }
        url = "https://api.paystack.co/transaction/initialize"
        response = requests.post(url, headers=headers, json=payload)
        return JsonResponse(response.json())


@csrf_exempt
def confirm_payment(request):
   if request.method == "GET":
        reference = request.GET.get("reference")
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        return JsonResponse(response.json())
