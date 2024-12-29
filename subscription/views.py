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
@login_required
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
            
            pk = settings.PAYSTACK_PUBLIC_KEY
            amount = plan.amount
            payment = Subscription.objects.create(amount=amount, phone_number=phone_number, user=request.user)
            payment.save()
            return JsonResponse({"message": "Payment created successfully.", "payment_id": payment.id}, status=201)
        
        
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error occurred: {str(e)}"}, status=500)


    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
@login_required
def confirm_payment(request, ref):
    try:
        payment = get_object_or_404(Payment, ref=ref)
        if payment.verify_payment():
            subscription = Subscription.objects.create(
                user=payment.user,
                plan=payment.plan,
                start_date=timezone.now()
            )
            duration = {
                "daily": timedelta(days=1),
                "monthly": timedelta(days=30),
                "yearly": timedelta(days=365),
            }.get(payment.plan.name, timedelta(days=0))
            subscription.end_date = subscription.start_date + duration
            subscription.save()
            return JsonResponse({"message": "Payment and subscription successful."}, status=200)
        else:
            return JsonResponse({"error": "Payment verification failed."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error occurred: {str(e)}"}, status=500)


# def check_subscription_status(request):
#     if request.user.is_authenticated:
#         subscription = Subscription.objects.filter(user=request.user).last()
#         if subscription and subscription.is_active():
#             return JsonResponse({"message": "Subscription is active."}, status=200)
#         else:
#             return JsonResponse({"message": "No active subscription."}, status=400)
#     else:
#         return JsonResponse({"error": "User not authenticated."}, status=403)

