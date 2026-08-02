"""
authentication/models.py
-------------------------
Django already gives us a built-in User model (username, email, password).
We don't rewrite it — instead we ATTACH a "Profile" to it, to hold extra
fields the built-in User doesn't have: phone number, and whether the user
wants Email or SMS price-drop alerts.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    notify_by_email = models.BooleanField(default=True)
    notify_by_sms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
