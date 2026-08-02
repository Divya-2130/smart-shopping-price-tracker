from django.urls import path
from .views import TrackProductView, MyTrackedProductsView

urlpatterns = [
    path("track/", TrackProductView.as_view(), name="track-product"),
    path("my-tracked/", MyTrackedProductsView.as_view(), name="my-tracked-products"),
]
