from django.contrib import admin
from .models import UserSubscription

# I register my model so I can edit it directly from the web interface
admin.site.register(UserSubscription)