from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # The landing page
    path('', views.index_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='subscriptions/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cancel/', views.cancel_subscription, name='cancel-plan'),
    path('upgrade/', views.upgrade_subscription, name='upgrade-plan'),
    # I define the dynamic URL path that expects a username string
    path('status/<str:username>/', views.get_user_subscription, name='subscription-status'),
    # I add the new POST endpoint to handle simulated payment webhooks
    path('webhook/payment/', views.payment_webhook, name='payment-webhook'),

]