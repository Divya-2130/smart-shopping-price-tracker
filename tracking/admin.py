from django.contrib import admin
from .models import TrackedProduct, PriceHistory

admin.site.register(TrackedProduct)
admin.site.register(PriceHistory)
