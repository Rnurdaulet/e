from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Только ADMIN может изменять, частично обновлять и удалять объекты.
    Остальные могут только читать (GET).
    """

    def has_permission(self, request, view):
        # Разрешаем всем аутентифицированным пользователям читать данные
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Только ADMIN может изменять
        return request.user.is_authenticated and request.user.role == request.user.Role.ADMIN
