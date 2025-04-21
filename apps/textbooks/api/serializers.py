from django.utils.timezone import now
from rest_framework import serializers
from ..models import Textbook, Introduction, Section, Lesson, Keyword
from ...subscriptions.models import Subscription


class TextbookSerializer(serializers.ModelSerializer):
    """Сериализатор для учебников"""
    is_accessible = serializers.SerializerMethodField()  # Проверяем доступ
    image = serializers.ImageField(required=False)

    class Meta:
        model = Textbook
        fields = ["id", "subject", "school_class", "language", "isbn", "title", "required_plan", "is_accessible","image"]

    def get_is_accessible(self, obj):
        """Определяем, доступен ли учебник пользователю"""
        user = self.context["request"].user

        # Если у учебника нет подписки — доступен всем
        if obj.required_plan is None:
            return True

        # Проверяем, есть ли у пользователя активная подписка на этот план
        has_subscription = Subscription.objects.filter(
            user=user,
            plan=obj.required_plan,
            end_date__gte=now()  # Подписка еще активна
        ).exists()

        return has_subscription


class IntroductionSerializer(serializers.ModelSerializer):
    """Сериализатор для введений в учебник"""

    class Meta:
        model = Introduction
        fields = ["id", "textbook", "text", "image"]


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для разделов учебника"""

    class Meta:
        model = Section
        fields = ["id", "textbook", "title", "text", "image"]


class KeywordSerializer(serializers.ModelSerializer):
    """Сериализатор для ключевых слов"""

    class Meta:
        model = Keyword
        fields = ["id", "text", "description"]


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = ["id", "section", "title", "objective", "description", "keywords", "quiz"]
