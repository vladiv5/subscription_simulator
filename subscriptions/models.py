from django.db import models
from django.contrib.auth.models import User

class UserSubscription(models.Model):
    # I link this model to the standard Django User (a 1-to-1 relationship)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    
    # I define the available access tiers in the application
    TIER_CHOICES = [
        ('FREE', 'Free Tier'),
        ('PREMIUM', 'Premium Tier'),
    ]
    
    # I set the default plan to be the free one
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='FREE')
    
    # I keep a simple flag to quickly check if the subscription is active
    is_active = models.BooleanField(default=True)
    
    # I add timestamps to know when the subscription was created or modified (useful for audit/growth)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # I format how the object will be displayed in the console and the admin panel
        return f"{self.user.username} - {self.tier} (Active: {self.is_active})"

# subscriptions/models.py

class PaymentTransaction(models.Model):
    # I link the transaction to the specific user using a One-to-Many relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # I record the amount paid
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # I store the tier they purchased
    tier_purchased = models.CharField(max_length=10)
    
    # I track exactly when the transaction happened
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # I keep track of the payment status
    status = models.CharField(max_length=20, default='SUCCESS')

    def __str__(self):
        # I format the transaction display for the admin panel
        return f"{self.user.username} - {self.tier_purchased} - {self.amount} ({self.status})"