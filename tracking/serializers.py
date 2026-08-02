from rest_framework import serializers
from .models import TrackedProduct, PriceHistory
from products.serializers import ProductSerializer


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ["price", "recorded_at"]


class TrackedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    price_history = PriceHistorySerializer(source="product.price_history", many=True, read_only=True)

    class Meta:
        model = TrackedProduct
        fields = ["id", "product", "last_known_price", "target_price", "price_history", "created_at"]
