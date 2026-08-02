"""
notifications/sms_service.py
------------------------------
Sends the actual SMS. Uses Twilio here as the example SMS API.
"""
from django.conf import settings
from twilio.rest import Client


def send_price_drop_sms(to_phone: str, product_name: str, new_price: float):
    body = f"Price Drop Alert: {product_name} now ₹{new_price}."

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=body,
            from_=settings.TWILIO_FROM_NUMBER,
            to=to_phone,
        )
    except Exception as e:
        # In production, log this instead of printing
        print(f"SMS send failed: {e}")
