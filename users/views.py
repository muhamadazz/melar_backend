from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, ChangePasswordSerializer
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi # type: ignore


class RegisterView(APIView):
    """Handle user registration and return relevant feedback."""
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user with email, username, phone number, full name, and password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User's email (must be unique)."),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Unique username for the user."),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="User's phone number (must be unique)."),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description="User's full name."),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Password for authentication."),
                'role': openapi.Schema(type=openapi.TYPE_STRING, enum=['admin', 'user'], description="User role (default: 'user')."),
                'is_seller': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Boolean indicating if the user is a seller (default: False)."),
            },
            required=['email', 'username', 'phone_number', 'full_name', 'password']
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                examples={
                    "application/json": {
                        "message": "User registered successfully.",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "username": "newuser",
                            "phone_number": "08123456789",
                            "full_name": "John Doe",
                            "role": "user",
                            "is_seller": False,
                            "is_active": True,
                            "created_at": "2025-03-19T12:00:00Z",
                            "updated_at": "2025-03-19T12:00:00Z"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Registration failed due to validation errors.",
                examples={
                    "application/json": {
                        "message": "Registration failed. Please check the provided data.",
                        "errors": {
                            "email": ["This field must be unique."],
                            "phone_number": ["This field must be unique."]
                        }
                    }
                }
            ),
        }
    )

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Registration failed. Please check the provided data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """Login using JWT and return access and refresh tokens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                "message": "Login successful.",
                "tokens": response.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Login failed. Please check your credentials."
        }, status=response.status_code)


class LogoutView(APIView):
    """Handle user logout by blacklisting their refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({
                "message": "Refresh token is missing in the request."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Assumes simplejwt.blacklist is configured
            return Response({
                "message": "Logout successful. Token has been blacklisted."
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "message": "Logout failed due to an invalid token.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve and update the authenticated user's profile."""
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current authenticated user."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Update the user's profile with feedback messages."""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Profile update failed. Please check the provided data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """API untuk mengubah password pengguna."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Menyimpan password baru setelah validasi berhasil
        serializer.save()
        
        return Response({"detail": "Password berhasil diubah."}, status=status.HTTP_200_OK)