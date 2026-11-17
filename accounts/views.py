import logging

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

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Невдала реєстрація: невалідні дані (поля: %s)",
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        logger.info(
            "Зареєстровано нового користувача: username=%s (id=%s)",
            user.username,
            user.id,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning("Спроба входу з невалідним форматом даних")
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data["username"]
        user = authenticate(
            username=username,
            password=serializer.validated_data["password"],
        )

        if user is None:
            logger.warning("Невдала спроба входу для username=%s", username)
            return Response(
                {"error": "Невірний username або пароль."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        logger.info(
            "Успішний вхід користувача: username=%s (id=%s)", user.username, user.id
        )
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
            logger.warning("Запит на оновлення токена без refresh-поля")
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(serializer.validated_data["refresh"])
        except TokenError:
            logger.warning(
                "Спроба оновити токен із недійсним або простроченим refresh-токеном"
            )
            return Response(
                {
                    "error": "Refresh токен недійсний або термін його дії закінчився. Увійдіть знову."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        logger.info("Оновлено access-токен для user_id=%s", refresh.get("user_id"))
        return Response({"access": str(refresh.access_token)})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug(
            "Запит профілю поточного користувача: username=%s", request.user.username
        )
        return Response(UserSerializer(request.user).data)
