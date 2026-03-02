from django.urls import path
from . import views

urlpatterns = [
    # I define the dynamic URL path that expects a username string
    path('status/<str:username>/', views.get_user_subscription, name='subscription-status'),
]