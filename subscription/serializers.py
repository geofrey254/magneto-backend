from rest_framework import serializers
from .models import Subscription, SubscriptionPlan, PaymentHistory

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

class paymentHistorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = PaymentHistory
        fields = ['user','amount_paid', 'reference_code', 'payment_date']

    def get_user(self, obj):
        # Return the username of the user
        return obj.user.username