from rest_framework import serializers
from django.utils.timezone import now
from ..models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    """Сериализатор для тарифных планов"""
    features = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ["id", "name", "plan_type", "price", "duration_days", "features"]

    def get_features(self, obj):
        # Исключаем чувствительные ключи
        excluded_keys = {"admin_note", "internal_code"}
        return {key: value for key, value in obj.features.items() if key not in excluded_keys}


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ["id", "plan", "school", "start_date", "end_date", "is_active"]
        read_only_fields = ["start_date", "end_date"]

    def get_is_active(self, obj):
        return obj.is_active()


class SubscriptionExtendSerializer(serializers.Serializer):
    """Сериализатор для продления подписки"""
    extra_days = serializers.IntegerField(min_value=1)
