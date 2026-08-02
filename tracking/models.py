"""
tracking/models.py
-------------------
TrackedProduct: which products a user wants to keep an eye on.
PriceHistory:   a log of every price we've recorded for a product,
                used to draw the price trend graph on the frontend.
"""
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class TrackedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracked_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    last_known_price = models.DecimalField(max_digits=10, decimal_places=2)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")  # a user can't track the same product twice

    def __str__(self):
        return f"{self.user.username} tracking {self.product.name}"


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["recorded_at"]

    def __str__(self):
        return f"{self.product.name} - ₹{self.price} on {self.recorded_at}"
