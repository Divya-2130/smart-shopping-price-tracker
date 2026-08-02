from django.urls import path
from .views import SearchView, CompareView

urlpatterns = [
    path("search/", SearchView.as_view(), name="product-search"),
    path("compare/", CompareView.as_view(), name="product-compare"),
]
