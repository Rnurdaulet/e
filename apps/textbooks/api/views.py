from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Textbook, Introduction, Section, Lesson, Keyword
from .serializers import TextbookSerializer, IntroductionSerializer, SectionSerializer, LessonSerializer, KeywordSerializer
from ...subscriptions.models import Subscription
from .permissions import IsAdminOrContentManager, HasSubscriptionOrFreeAccess


class TextbookViewSet(viewsets.ModelViewSet):
    """API для учебников"""
    queryset = Textbook.objects.all()
    serializer_class = TextbookSerializer
    permission_classes = [HasSubscriptionOrFreeAccess]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subject", "school_class", "language"]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Фильтруем список учебников по подписке"""
        user = self.request.user
        queryset = Textbook.objects.all()

        if user.role == user.Role.ADMIN:
            return queryset

        # Получаем подписки пользователя
        active_plans = Subscription.objects.filter(user=user, end_date__gte=now()).values_list("plan", flat=True)

        # Доступны все бесплатные учебники + учебники по подписке
        return queryset.filter(required_plan__isnull=True) | queryset.filter(required_plan__in=active_plans)


class IntroductionViewSet(viewsets.ModelViewSet):
    """API для введений"""
    queryset = Introduction.objects.all()
    serializer_class = IntroductionSerializer
    permission_classes = [HasSubscriptionOrFreeAccess]

    def get_queryset(self):
        """Фильтруем введения по доступности учебника"""
        user = self.request.user
        available_textbooks = Textbook.objects.filter(required_plan__isnull=True) | Textbook.objects.filter(
            required_plan__in=Subscription.objects.filter(user=user, end_date__gte=now()).values_list("plan", flat=True)
        )
        return Introduction.objects.filter(textbook__in=available_textbooks)


class SectionViewSet(viewsets.ModelViewSet):
    """API для разделов"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [HasSubscriptionOrFreeAccess]

    def get_queryset(self):
        """Фильтруем разделы по доступности учебника"""
        user = self.request.user
        available_textbooks = Textbook.objects.filter(required_plan__isnull=True) | Textbook.objects.filter(
            required_plan__in=Subscription.objects.filter(user=user, end_date__gte=now()).values_list("plan", flat=True)
        )
        return Section.objects.filter(textbook__in=available_textbooks)


class LessonViewSet(viewsets.ModelViewSet):
    """API для уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [HasSubscriptionOrFreeAccess]

    def get_queryset(self):
        """Фильтруем уроки по доступности учебника"""
        user = self.request.user
        available_textbooks = Textbook.objects.filter(required_plan__isnull=True) | Textbook.objects.filter(
            required_plan__in=Subscription.objects.filter(user=user, end_date__gte=now()).values_list("plan", flat=True)
        )
        return Lesson.objects.filter(section__textbook__in=available_textbooks)


class KeywordViewSet(viewsets.ModelViewSet):
    """API для ключевых слов"""
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [HasSubscriptionOrFreeAccess]
