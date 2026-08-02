"""
products/models.py
-------------------
We cache products locally in MySQL so that:
  1. Repeated searches for the same item are faster.
  2. Modules like Tracking and Wishlist can reference a stable product_id
     instead of calling RapidAPI every single time.
"""
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    seller = models.CharField(max_length=100)          # e.g. "Amazon", "Flipkart"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    product_link = models.URLField(max_length=500)      # link to the real product page
    external_id = models.CharField(max_length=255, blank=True, null=True)  # ID from RapidAPI, if provided
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.seller}) - ₹{self.price}"
