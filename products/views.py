"""
products/views.py
------------------
Two endpoints:
  - SearchView:  GET /api/products/search/?q=iphone15
  - CompareView: GET /api/products/compare/?q=iphone15  (same data, sorted by price)
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import rapidapi_service
from .models import Product
from .serializers import ProductSerializer


class SearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "Missing search query 'q'"}, status=status.HTTP_400_BAD_REQUEST)

        results = rapidapi_service.search_products(query)

        # Cache each result in MySQL so tracking/wishlist can reference it later
        saved_products = []
        for item in results:
            product, _ = Product.objects.update_or_create(
                external_id=item["external_id"],
                seller=item["seller"],
                defaults={
                    "name": item["name"],
                    "price": item["price"],
                    "image_url": item["image_url"],
                    "product_link": item["product_link"],
                },
            )
            saved_products.append(product)

        return Response({"results": ProductSerializer(saved_products, many=True).data})


class CompareView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "Missing search query 'q'"}, status=status.HTTP_400_BAD_REQUEST)

        results = rapidapi_service.search_products(query)
        sorted_results = sorted(results, key=lambda item: item["price"])

        for i, item in enumerate(sorted_results):
            item["cheapest"] = (i == 0)

        return Response({"comparison": sorted_results})
