from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает только чтение, кроме случаев, когда пользователь — администратор.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Разрешить чтение всем
        return request.user.is_authenticated and request.user.role == request.user.Role.ADMIN


class SubscriptionPermissions(permissions.BasePermission):
    """
    Разрешает:
    - `ADMIN` — полный доступ.
    - `SCHOOL_ADMIN` — просмотр подписок своей школы.
    - Остальные могут только просматривать свои подписки и продлевать их.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == request.user.Role.ADMIN:
            return True  # Полные права у ADMIN

        if request.method in permissions.SAFE_METHODS:
            if request.user.role == request.user.Role.SCHOOL_ADMIN:
                return obj.school == request.user.school  # SCHOOL_ADMIN видит подписки своей школы
            return obj.user == request.user  # Остальные видят только свои подписки

        if view.action == "extend":
            return obj.user == request.user  # Разрешить продление подписки

        return False  # Изменение/удаление запрещено
