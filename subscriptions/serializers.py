from rest_framework import serializers
from .models import UserSubscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        # I specify the model I want to serialize
        model = UserSubscription
        # I select only the safe fields to expose in my API response
        fields = ['tier', 'is_active', 'created_at']