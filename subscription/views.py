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
from django_daraja.mpesa.core import MpesaClient




class subscriptionPlanViewset(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = subscriptionPlanSerializer
    filter_backends = [DjangoFilterBackend]

class subscriptionViewset(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = subscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'plan'


# def push_stk(request):
#     cl = MpesaClient()
#     phone_number = '0742954513'
#     amount = 1
#     account_reference = 'reference'
#     transaction_desc = 'Description'
#     callback_url = 'https://api.darajambili.com/express-payment'
#     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#     return HttpResponse(response)

# def stk_push_callback(request):
#         data = request.body
        
#         return HttpResponse("STK Push in Django👋")
@login_required
def debug_login_status(request):
    return JsonResponse({"user": request.user.username, "is_authenticated": request.user.is_authenticated})

@csrf_exempt
def submit_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data)
            
            plan_id = data.get("plan_id")
            phone_number = data.get("phone_number")
            print(f"Plan ID: {plan_id}, Phone Number: {phone_number}")

            if not plan_id:
                return JsonResponse({"error": "Invalid plan ID."}, status=400)

            plan = get_object_or_404(SubscriptionPlan, id=plan_id)
            print(f"Fetched Plan: {plan}")

            cl = MpesaClient()
            amount = plan.price
            account_reference = f"Subscription_{plan.name}"
            transaction_desc = "Subscription Payment"
            callback_url = 'https://209d-41-90-40-205.ngrok-free.app/subscription/callback'
            print("Initiating STK push...")

            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            print("Mpesa Response:", response)

            if hasattr(response, 'response_code') and response.response_code == "0":
                duration = {
                    'daily': timedelta(days=1),
                    'monthly': timedelta(days=30),
                    'yearly': timedelta(days=365),
                }.get(plan.name, timedelta(days=1))
                print("Calculated Duration:", duration)

                if request.user.is_authenticated:
                    subscription = Subscription.objects.create(
                        user=request.user,
                        plan=plan,
                        start_date=timezone.now(),
                        end_date=timezone.now() + duration
                    )
                    print("Created Subscription:", subscription)

                    request.session['is_subscribed'] = subscription.is_active()

                    return JsonResponse({"message": "Payment initiated. Awaiting confirmation."}, status=200)
                else:
                    print("User not authenticated.")
                    return JsonResponse({"error": "User is not authenticated."}, status=403)
            else:
                error_message = response.response_description or response.error_message
                print("STK Push Error:", error_message)
                return JsonResponse({
                    "message": "Failed to initiate payment", 
                    "error": error_message
                }, status=500)

        except Exception as e:
            print("Unexpected Error:", str(e))
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def confirm_payment(request):
    """Handles M-Pesa callback for payment confirmation."""
    if request.method == "POST":
        data = json.loads(request.body)

        transaction_status = data.get("ResultCode")
        phone_number = data.get("phone_number")

        if transaction_status == "0":  # Payment successful
            subscription = Subscription.objects.filter(user__phone_number=phone_number, status="Pending").last()
            if subscription:
                duration = {
                    'daily': timedelta(days=1),
                    'monthly': timedelta(days=30),
                    'yearly': timedelta(days=365),
                }.get(subscription.plan.name, timedelta(days=1))

                subscription.status = "Active"
                subscription.start_date = timezone.now()
                subscription.end_date = timezone.now() + duration
                subscription.save()
                return JsonResponse({"message": "Payment confirmed, subscription active."}, status=200)

        return JsonResponse({"message": "Payment failed."}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def check_subscription_status(request):
    if request.user.is_authenticated:
        subscription = Subscription.objects.filter(user=request.user).last()
        if subscription and subscription.is_active():
            return JsonResponse({"message": "Subscription is active."}, status=200)
        else:
            return JsonResponse({"message": "No active subscription."}, status=400)
    else:
        return JsonResponse({"error": "User not authenticated."}, status=403)

