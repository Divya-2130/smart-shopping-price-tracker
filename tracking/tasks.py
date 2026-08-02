"""
tracking/tasks.py
------------------
This is the automatic background job (Module 3's core logic).
It runs on a schedule (see CELERY_BEAT_SCHEDULE in settings.py — every 6 hours)
without any user clicking a button.

For each tracked product:
  1. Ask RapidAPI for the current price.
  2. Save it into PriceHistory (so the price graph grows over time).
  3. If the price dropped (or hit the user's target), trigger a notification.
"""
from celery import shared_task
from products import rapidapi_service
from .models import TrackedProduct, PriceHistory
from notifications.email_service import send_price_drop_email
from notifications.sms_service import send_price_drop_sms
from notifications.models import Notification


@shared_task
def check_prices_job():
    tracked_items = TrackedProduct.objects.select_related("product", "user__profile")

    for tracked in tracked_items:
        try:
            current_price = rapidapi_service.get_current_price(tracked.product.product_link)
        except Exception as e:
            # In production, log this properly instead of printing
            print(f"Price check failed for {tracked.product.name}: {e}")
            continue

        PriceHistory.objects.create(product=tracked.product, price=current_price)

        price_dropped = current_price < float(tracked.last_known_price)
        hit_target = tracked.target_price and current_price <= float(tracked.target_price)

        if price_dropped or hit_target:
            notify_user(tracked, current_price)

        tracked.product.price = current_price
        tracked.product.save()
        tracked.last_known_price = current_price
        tracked.save()


def notify_user(tracked_product, new_price):
    """Sends the alert and logs it — this is Module 5's entry point."""
    user = tracked_product.user
    product = tracked_product.product
    message = f"Price Drop Alert! {product.name} is now ₹{new_price} (was ₹{tracked_product.last_known_price})"

    profile = getattr(user, "profile", None)

    if profile and profile.notify_by_email:
        send_price_drop_email(user.email, product.name, new_price, tracked_product.last_known_price)

    if profile and profile.notify_by_sms and profile.phone_number:
        send_price_drop_sms(profile.phone_number, product.name, new_price)

    Notification.objects.create(user=user, message=message)
