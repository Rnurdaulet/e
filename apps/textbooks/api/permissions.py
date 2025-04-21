from rest_framework import permissions
from django.utils.timezone import now
from apps.subscriptions.models import Subscription


class IsAdminOrContentManager(permissions.BasePermission):
    """
    Только ADMIN и CONTENT_MANAGER могут изменять данные.
    Остальные могут только читать.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            request.user.Role.ADMIN,
            request.user.Role.CONTENT_MANAGER,
        ]


class HasSubscriptionOrFreeAccess(permissions.BasePermission):
    """
    - Пользователи могут читать только учебники, на которые у них есть подписка.
    - Бесплатные учебники (без `required_plan`) доступны всем.
    - `ADMIN` видит все.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            request.user.Role.ADMIN,
            request.user.Role.CONTENT_MANAGER,
        ]

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == user.Role.ADMIN:
            return True  # `ADMIN` видит все

        # Если учебник бесплатный — доступен всем
        if obj.required_plan is None:
            return True

        # Проверка подписки
        return Subscription.objects.filter(
            user=user,
            plan=obj.required_plan,
            end_date__gte=now()
        ).exists()
