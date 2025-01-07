from rest_framework import serializers
from .models import Subscription, SubscriptionPlan

class subscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class subscriptionSerializer(serializers.ModelSerializer): 
    plan = serializers.CharField(source='plan.name', read_only=True)
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['slug']

