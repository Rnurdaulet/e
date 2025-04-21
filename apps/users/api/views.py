from dj_rest_auth.views import LoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .permissions import UserPermissions
from .serializers import (
    UserSerializer,
    UserProfileSerializer, CustomRegisterSerializer
)
from ..models import UserProfile, CustomUser

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями (CRUD с ролевыми ограничениями)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        """Фильтруем пользователей по школе, если роль требует этого"""
        user = self.request.user

        if user.role in [CustomUser.Role.SCHOOL_ADMIN, CustomUser.Role.TEACHER, CustomUser.Role.EXPERT]:
            return User.objects.filter(school=user.school)

        return super().get_queryset()

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Возвращает данные текущего пользователя"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Запрещаем создание пользователей, если роль не ADMIN или SCHOOL_ADMIN"""
        user = self.request.user

        if user.role not in [User.Role.ADMIN, User.Role.SCHOOL_ADMIN]:
            return Response({"error": "Вы не можете создавать пользователей."}, status=status.HTTP_403_FORBIDDEN)

        new_user_role = serializer.validated_data.get("role")
        if user.role == User.Role.SCHOOL_ADMIN and new_user_role not in [User.Role.TEACHER, User.Role.STUDENT]:
            return Response({"error": "Вы можете создавать только учителей и учеников."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.validated_data["school"] = user.school
        serializer.save()

    def perform_destroy(self, instance):
        """Запрещаем удаление, если нет прав"""
        user = self.request.user

        if user.role not in [User.Role.ADMIN, User.Role.SCHOOL_ADMIN]:
            return Response({"error": "Вы не можете удалять пользователей."}, status=status.HTTP_403_FORBIDDEN)

        if user.role == User.Role.SCHOOL_ADMIN:
            #  SCHOOL_ADMIN не может удалить себя
            if instance == user:
                return Response({"error": "Вы не можете удалить свою учетную запись."},
                                status=status.HTTP_403_FORBIDDEN)

            #  SCHOOL_ADMIN может удалять только TEACHER и STUDENT своей школы
            if instance.role not in [User.Role.TEACHER, User.Role.STUDENT] or instance.school != user.school:
                return Response({"error": "Вы можете удалять только учителей и учеников своей школы."},
                                status=status.HTTP_403_FORBIDDEN)

        instance.delete()


class UserProfileViewSet(viewsets.ModelViewSet):
    """Управление профилями пользователей"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserPermissions]


class CustomLoginView(LoginView):
    """Кастомный вход с записью refresh-токена в cookie"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Проверяем, залогинен ли пользователь
        if response.status_code == 200:
            user = self.user  # Пользователь, прошедший аутентификацию
            refresh = RefreshToken.for_user(user)  # Генерируем токены
            access = str(refresh.access_token)

            # Устанавливаем refresh-токен в HTTP-only cookie
            response.set_cookie(
                key=settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH", "refresh_token"),
                value=str(refresh),
                httponly=True,
                secure=True,  # Включить, если HTTPS
                samesite="Lax"
            )

            # Устанавливаем access-токен в HTTP-only cookie
            response.set_cookie(
                key=settings.SIMPLE_JWT.get("AUTH_COOKIE", "access_token"),
                value=access,
                httponly=True,
                secure=True,
                samesite="Lax"
            )

            # Принудительно добавляем refresh в JSON-ответ
            response.data["refresh"] = str(refresh)

        return response


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        """Обрабатываем регистрацию пользователя"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "phone": user.phone,
                "iin": user.iin
            },
            status=status.HTTP_201_CREATED
        )
