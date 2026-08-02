"""
authentication/serializers.py
------------------------------
A "serializer" is a translator: it converts JSON (sent by React) into
Python/Django objects, and validates the data (e.g. is the email format
correct? is the password long enough?).
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    phone_number = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone_number"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        phone_number = validated_data.pop("phone_number", "")
        # create_user() automatically hashes the password — never store plain text
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        UserProfile.objects.create(user=user, phone_number=phone_number)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["username", "email", "phone_number", "notify_by_email", "notify_by_sms"]
