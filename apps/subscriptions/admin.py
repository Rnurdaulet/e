from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    """ Управление тарифными планами """
    list_display = ("name", "plan_type", "price", "duration_days")
    list_filter = ("plan_type",)
    search_fields = ("name",)
    readonly_fields = ("id",)
    fieldsets = (
        ("Основное", {"fields": ("name", "plan_type", "price", "duration_days")}),
        ("Дополнительно", {"fields": ("features",)}),
    )


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    """ Управление подписками пользователей и школ """
    list_display = ("user", "school", "plan", "start_date", "end_date", "is_active")
    search_fields = ("user__username", "school__name")
    list_filter = ("plan__plan_type", "start_date", "end_date")
    readonly_fields = ("id", "start_date")

    fieldsets = (
        ("Общая информация", {"fields": ("plan", "start_date", "end_date")}),
        ("Привязка", {"fields": ("user", "school")}),
    )

    def is_active(self, obj):
        return obj.is_active()

    is_active.boolean = True  # Отображать в виде флажка ✅/❌
