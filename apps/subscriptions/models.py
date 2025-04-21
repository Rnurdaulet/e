from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from apps.education.models import School  # Импорт вашей модели школы

User = get_user_model()


class Plan(models.Model):
    """Тарифные планы (персональные и корпоративные)"""
    TYPE_CHOICES = [
        ("personal", "Персональная"),
        ("corporate", "Корпоративная"),
    ]

    name = models.CharField(max_length=100, verbose_name="Название плана")
    plan_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип подписки")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_days = models.IntegerField(verbose_name="Длительность (дни)")
    features = models.JSONField(default=dict, verbose_name="Особенности")  # Например, {"max_courses": 5}

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"


class Subscription(models.Model):
    """Модель подписки (привязка к пользователю или школе)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Школа")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name="Тарифный план")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")

    def is_active(self):
        return self.end_date >= now()

    def extend(self, extra_days):
        self.end_date += timedelta(days=extra_days)
        self.save()

    def __str__(self):
        if self.user:
            return f"Подписка {self.plan.name} для {self.user}"
        elif self.school:
            return f"Подписка {self.plan.name} для {self.school.name}"
        return "Неизвестная подписка"
