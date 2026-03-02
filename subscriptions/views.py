from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserSubscription
from .serializers import SubscriptionSerializer
from .models import UserSubscription, PaymentTransaction
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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

def index_view(request):
    username = request.GET.get('user')
    context = {}

    # I handle the admin search functionality first
    if username:
        try:
            sub = UserSubscription.objects.get(user__username=username)
            context['result'] = {
                'username': sub.user.username,
                'tier': sub.tier,
                'is_active': sub.is_active
            }
        except UserSubscription.DoesNotExist:
            context['error'] = "User not found."

    # I extract my own subscription fresh from the database to bypass any frontend caching
    if request.user.is_authenticated and not request.user.is_superuser:
        # I use filter().first() to safely grab the active subscription directly from the DB
        context['my_subscription'] = UserSubscription.objects.filter(user=request.user).first()

    return render(request, 'subscriptions/status.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # I save the new user and automatically log them in
            user = form.save()
            # I also ensure they have a default FREE subscription
            UserSubscription.objects.create(user=user, tier='FREE')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'subscriptions/register.html', {'form': form})

@login_required
def upgrade_subscription(request):
    if request.method == 'POST':
        target_username = request.POST.get('username')
        
        # I check if I am an admin trying to upgrade another user
        if target_username and request.user.is_superuser:
            sub = UserSubscription.objects.get(user__username=target_username)
            redirect_url = f'/api/subscriptions/?user={target_username}'
        else:
            # I force the system to only upgrade my own account if I am a regular user
            sub = UserSubscription.objects.get(user=request.user)
            redirect_url = 'home'

        if sub.tier == 'FREE':
            sub.tier = 'PREMIUM'
            sub.save()
            # I log the transaction
            PaymentTransaction.objects.create(
                user=sub.user, amount=9.99, tier_purchased='PREMIUM', status='COMPLETED'
            )
            
        return redirect(redirect_url)
    return redirect('home')

@login_required
def cancel_subscription(request):
    if request.method == 'POST':
        target_username = request.POST.get('username')
        
        # I check if I am an admin trying to downgrade another user
        if target_username and request.user.is_superuser:
            sub = UserSubscription.objects.get(user__username=target_username)
            redirect_url = f'/api/subscriptions/?user={target_username}'
        else:
            # I force the system to only downgrade my own account if I am a regular user
            sub = UserSubscription.objects.get(user=request.user)
            redirect_url = 'home'
            
        if sub.tier == 'PREMIUM':
            sub.tier = 'FREE'
            sub.save()
            # I log the cancellation
            PaymentTransaction.objects.create(
                user=sub.user, amount=0, tier_purchased='FREE', status='CANCELLED'
            )
            
        return redirect(redirect_url)
    return redirect('home')