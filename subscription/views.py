import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import subscriptionPlanSerializer, subscriptionSerializer
from .models import Subscription, SubscriptionPlan
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import requests
from django.contrib.auth.models import User


class subscriptionPlanViewset(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = subscriptionPlanSerializer
    filter_backends = [DjangoFilterBackend]

class subscriptionViewset(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = subscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'plan'

@permission_classes([IsAuthenticated])  
def submit_payment(request, plan_id):    
    if request.method == "POST":
        
        data = json.loads(request.body)
        amount = int(data.get("amount")) * 100
        email = data.get("email")
        
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        user = data.get("user")
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": email,
            "amount": amount,
            "metadata": {"plan_id": plan.id, "user": email},
            "callback_url": "http://localhost:3000/subscription/success",
        }
        url = "https://api.paystack.co/transaction/initialize"
        response = requests.post(url, headers=headers, json=payload)
        return JsonResponse(response.json())

@csrf_exempt
def confirm_payment(request):
    if request.method == "POST":
        reference = request.GET.get("reference")
        if not reference:
            return JsonResponse({'status': 'error', 'message': 'Reference is required'}, status=400)

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data['status'] == True:
            plan_id = response_data['data']['metadata']['plan_id']
            user_email = response_data['data']['customer']['email']
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id)
            except SubscriptionPlan.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Subscription plan not found'}, status=404)

            try:
                # Get the user by email
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)           
           
            existing_subscription = Subscription.objects.filter(user=user, plan=plan).first()
            if existing_subscription and existing_subscription.verified:
                    return JsonResponse({'status': 'error', 'message': 'User already subscribed to this plan'}, status=400)   
            Subscription.objects.create(plan=plan, user=user, verified=True)

            return JsonResponse({'status': 'success', 'message': 'Payment verified and subscription created'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment verification failed'}, status=400)