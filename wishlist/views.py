from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user)
        return Response(WishlistItemSerializer(items, many=True).data)

    def post(self, request):
        product_id = request.data.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        return Response(
            WishlistItemSerializer(item).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def delete(self, request):
        product_id = request.query_params.get("product_id")
        WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
        return Response({"status": "removed"}, status=status.HTTP_204_NO_CONTENT)
