from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class LogoutView(TokenBlacklistView):
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)
