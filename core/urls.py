from django.contrib import admin
from django.urls import path, include # I import 'include' here
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # I connect all the URLs from my subscriptions app under the /api/ prefix
    path('api/subscriptions/', include('subscriptions.urls')), 

    # I redirect the absolute root URL of my project straight to the subscriptions dashboard
    path('', RedirectView.as_view(url='/api/subscriptions/', permanent=False)),

    # I add the endpoints for generating and refreshing JWT tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
