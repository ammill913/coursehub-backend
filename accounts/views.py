from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    RefreshSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return Response(
                {"error": "Невірний username або пароль."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )


class RefreshView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(serializer.validated_data["refresh"])
        except TokenError:
            return Response(
                {
                    "error": "Refresh токен недійсний або термін його дії закінчився. Увійдіть знову."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response({"access": str(refresh.access_token)})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
