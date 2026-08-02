"""
tracking/views.py
------------------
  - TrackProductView: POST here to start tracking a product (or set a target price)
  - MyTrackedProductsView: GET here to see everything you're tracking, with price history
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import TrackedProduct, PriceHistory
from .serializers import TrackedProductSerializer


class TrackProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        target_price = request.data.get("target_price")  # optional

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        tracked, created = TrackedProduct.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"last_known_price": product.price, "target_price": target_price},
        )
        if not created:
            tracked.target_price = target_price or tracked.target_price
            tracked.save()

        # Log today's price into history the moment tracking starts
        PriceHistory.objects.get_or_create(product=product, price=product.price)

        return Response(TrackedProductSerializer(tracked).data, status=status.HTTP_201_CREATED)


class MyTrackedProductsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tracked_items = TrackedProduct.objects.filter(user=request.user)
        return Response(TrackedProductSerializer(tracked_items, many=True).data)

    def delete(self, request):
        product_id = request.query_params.get("product_id")
        TrackedProduct.objects.filter(user=request.user, product_id=product_id).delete()
        return Response({"status": "removed"}, status=status.HTTP_204_NO_CONTENT)
