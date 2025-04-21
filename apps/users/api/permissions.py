from rest_framework.permissions import BasePermission
from apps.users.models import CustomUser


class UserPermissions(BasePermission):
    """
    Разрешения на основе ролей CustomUser.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == CustomUser.Role.ADMIN:
            return True  # Полный доступ

        if user.role == CustomUser.Role.SCHOOL_ADMIN:
            return view.action in ["list", "retrieve", "update", "partial_update", "destroy", "me"]

        if user.role == CustomUser.Role.TEACHER:
            return view.action in ["list", "retrieve", "update", "partial_update", "me"]

        if user.role == CustomUser.Role.EXPERT:
            return view.action in ["list", "retrieve", "update", "partial_update", "me"]

        if user.role == CustomUser.Role.CONTENT_MANAGER:
            return view.action in ["me", "change_password"]

        if user.role == CustomUser.Role.USER:
            return view.action in ["me", "change_password"]

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == CustomUser.Role.ADMIN:
            return obj != user

        if user.role == CustomUser.Role.SCHOOL_ADMIN:
            return obj.role in [CustomUser.Role.TEACHER, CustomUser.Role.STUDENT] and obj.school == user.school

        if user.role == CustomUser.Role.TEACHER:
            return obj.role == CustomUser.Role.STUDENT and obj.school == user.school

        if user.role == CustomUser.Role.EXPERT:
            return obj.role == CustomUser.Role.STUDENT and obj.school == user.school or obj == user

        if user.role == CustomUser.Role.CONTENT_MANAGER:
            return obj == user

        if user.role == CustomUser.Role.USER:
            return obj == user

        return False
