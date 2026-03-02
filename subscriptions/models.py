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