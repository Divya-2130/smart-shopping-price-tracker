"""
authentication/views.py
------------------------
Views are the actual functions that run when React calls an API endpoint.
This file handles: register, login (returns a JWT token), and viewing/
updating your own profile (e.g. turning SMS alerts on/off).
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserProfileSerializer
from .models import UserProfile


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"status": "success", "message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate

        email = request.data.get("email")
        password = request.data.get("password")

        # Django's default authenticate() checks username, so we look up
        # the username by email first.
        from django.contrib.auth.models import User
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user_obj.username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "success",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {"id": user.id, "username": user.username},
        })


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)

    def put(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.notify_by_email = request.data.get("notify_by_email", profile.notify_by_email)
        profile.notify_by_sms = request.data.get("notify_by_sms", profile.notify_by_sms)
        profile.phone_number = request.data.get("phone_number", profile.phone_number)
        profile.save()
        return Response(UserProfileSerializer(profile).data)
