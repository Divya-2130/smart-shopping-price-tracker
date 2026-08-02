from django.core.mail import send_mail
from django.conf import settings


def send_price_drop_email(to_email: str, product_name: str, new_price: float, old_price: float):
    subject = f"Price Drop Alert: {product_name}"
    body = (
        f"Good news! The price of {product_name} dropped to ₹{new_price} "
        f"(was ₹{old_price}). Check it out before the price goes back up!"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email send failed: {e}")