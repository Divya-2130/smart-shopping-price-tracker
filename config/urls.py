"""
config/urls.py
---------------
This is the master route table. Every module's urls.py is "plugged in"
here under a prefix, e.g. everything in authentication/urls.py becomes
reachable under /api/auth/...
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("authentication.urls")),
    path("api/products/", include("products.urls")),
    path("api/tracking/", include("tracking.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/wishlist/", include("wishlist.urls")),
]
