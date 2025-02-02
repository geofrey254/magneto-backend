import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import subscriptionPlanSerializer, subscriptionSerializer, paymentHistorySerializer
from .models import Subscription, SubscriptionPlan, PaymentHistory
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class subscriptionPlanViewset(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = subscriptionPlanSerializer
    filter_backends = [DjangoFilterBackend]

    @method_decorator(cache_page(60 * 15))  # Cache list action
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # Cache retrieve action
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class subscriptionViewset(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = subscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'plan'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user:
            raise PermissionDenied("User not authenticated")
        return self.queryset.filter(user=user)
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        # Serialize the QuerySet to JSON format
        queryset = self.get_queryset()
        # Check if the subscriptions have expired and update the status if necessary
        now = timezone.now()  # Get the current time
        subscriptions_to_update = []  # Track subscriptions to update

        for subscription in queryset:
            # Check if the subscription has expired
            if subscription.end_date < now and subscription.is_active:
                subscription.verified = False
                subscriptions_to_update.append(subscription)

        # Save the updates to expired subscriptions
        if subscriptions_to_update:
            Subscription.objects.bulk_update(
                subscriptions_to_update, ['verified'])

        serializer = self.get_serializer(queryset, many=True)

        # Log the serialized data to check the format
        print(serializer.data)

        # Return the serialized data correctly in JsonResponse
        return JsonResponse({'subscriptions': serializer.data})


@permission_classes([IsAuthenticated])
def submit_payment(request, plan_id):
    if request.method == "POST":
        print(request.headers)

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

            existing_subscription = Subscription.objects.filter(
                user=user, plan=plan).first()
            if existing_subscription and existing_subscription.verified:
                return JsonResponse({'status': 'error', 'message': 'User already subscribed to this plan'}, status=400)
            Subscription.objects.create(plan=plan, user=user, verified=True)
            PaymentHistory.objects.create(
                user=user, amount_paid=plan.amount, reference_code=reference, payment_date=timezone.now())
            print(f"Created subscription for user: {
                  user.email}, plan: {plan.name}")

            return JsonResponse({'status': 'success', 'message': 'Payment verified and subscription created'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment verification failed'}, status=400)

class paymentHistoryViewset(viewsets.ModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = paymentHistorySerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'reference_code'
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15))  # Cache list action
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # Cache retrieve action
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user:
            raise PermissionDenied("User not authenticated")
        return self.queryset.filter(user=user)

