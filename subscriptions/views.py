from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserSubscription
from .serializers import SubscriptionSerializer
from .models import UserSubscription, PaymentTransaction

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

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # I lock this endpoint so only users with a valid token can access it
def payment_webhook(request):
    # I extract the username and the new tier from the incoming JSON payload
    username = request.data.get('username')
    new_tier = request.data.get('tier')

    # I validate that both fields are present in the request
    if not username or not new_tier:
        return Response({"error": "Both 'username' and 'tier' are required."}, status=400)

    try:
        # I fetch the user's subscription from the database
        subscription = UserSubscription.objects.get(user__username=username)
        
        # I update the subscription details
        subscription.tier = new_tier.upper()
        subscription.is_active = True
        
        # I save the changes directly to PostgreSQL
        subscription.save()

        # I record the payment transaction in the database
        PaymentTransaction.objects.create(
            user=subscription.user,
            amount=9.99, # I hardcode the price for this simulation
            tier_purchased=new_tier.upper(),
            status='SUCCESS'
        )
        
        # I use the serializer to format the updated data for the response
        serializer = SubscriptionSerializer(subscription)
        
        return Response({
            "message": "Payment successful. Subscription updated.",
            "data": serializer.data
        }, status=200)
        
    except UserSubscription.DoesNotExist:
        # I return an error if the user doesn't exist
        return Response({"error": "Subscription not found for this user."}, status=404)