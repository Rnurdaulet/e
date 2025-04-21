from rest_framework import permissions


class IsAdminOrContentManager(permissions.BasePermission):
    """
    Только ADMIN и CONTENT_MANAGER могут изменять, удалять тестовые данные.
    Остальные могут только читать.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            request.user.Role.ADMIN,
            request.user.Role.CONTENT_MANAGER,
        ]


class IsOwnerOrSchoolAdmin(permissions.BasePermission):
    """
    - Пользователь (`USER`, `STUDENT`) может видеть только свои ответы.
    - `EXPERT`, `TEACHER`, `SCHOOL_ADMIN` могут видеть ответы своей школы.
    - `ADMIN` может видеть все.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == request.user.Role.ADMIN:
            return True  # `ADMIN` видит все

        if request.user.role in [request.user.Role.EXPERT, request.user.Role.TEACHER, request.user.Role.SCHOOL_ADMIN]:
            return obj.user.school == request.user.school  # Видят ответы своей школы

        return obj.user == request.user  # Обычные пользователи видят только свои данные
