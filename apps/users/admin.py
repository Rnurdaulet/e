from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import action
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("id", "avatar_preview", "email", "first_name", "last_name", "role", "is_active", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name", "iin")
    ordering = ("-date_joined",)
    list_editable = ("is_active",)
    readonly_fields = ("date_joined", "updated_at")
    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        ("Основная информация", {"fields": ("email", "password", "role")}),
        ("Персональные данные", {"fields": ("first_name", "last_name", "iin", "phone", "avatar")}),
        ("Статус", {"fields": ("is_active", "is_staff", "is_superuser", "has_full_access")}),
        ("Дополнительная информация", {"fields": ("date_joined", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    actions = ["activate_users", "deactivate_users"]

    @action(description="Сделать выбранных пользователей активными")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @action(description="Сделать выбранных пользователей неактивными")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    def avatar_preview(self, obj):
        """Отображение миниатюры аватара"""
        if obj.avatar:
            return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;" />', obj.avatar.url)
        return "-"

    avatar_preview.short_description = "Аватар"


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ("user", "school", "language", "school_class", "subject")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("school", "language", "subject")
