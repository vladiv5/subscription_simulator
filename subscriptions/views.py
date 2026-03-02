from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserSubscription
from .serializers import SubscriptionSerializer

@api_view(['GET'])
def get_user_subscription(request, username):
    # I try to fetch the subscription for the requested username from the database
    try:
        subscription = UserSubscription.objects.get(user__username=username)
        
        # I pass the database object to my serializer to convert it to JSON
        serializer = SubscriptionSerializer(subscription)
        
        # I return the JSON response with a 200 OK status automatically
        return Response(serializer.data)
        
    except UserSubscription.DoesNotExist:
        # I return a clean error message and a 404 status if nothing is found
        return Response({"error": "Subscription not found for this user"}, status=404)