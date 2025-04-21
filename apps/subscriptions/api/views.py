import logging
from datetime import timedelta
from django.utils.timezone import now
from django.core.cache import cache
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly, SubscriptionPermissions
from .serializers import PlanSerializer, SubscriptionSerializer, SubscriptionExtendSerializer
from ..models import Plan, Subscription

logger = logging.getLogger(__name__)

class PlanViewSet(viewsets.ModelViewSet):
    """CRUD API для тарифных планов (доступно только администраторам)"""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """CRUD API для подписок"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, SubscriptionPermissions]

    def get_queryset(self):
        """Фильтруем подписки в зависимости от роли"""
        user = self.request.user

        if user.is_superuser or user.role == user.Role.ADMIN:
            return Subscription.objects.all()

        if user.role == user.Role.SCHOOL_ADMIN:
            return Subscription.objects.filter(school=user.school)

        return Subscription.objects.filter(user=user)

    def perform_create(self, serializer):
        """Запрещаем дублирование подписок и манипуляцию ценами"""
        user = self.request.user

        if Subscription.objects.filter(user=user, end_date__gte=now()).exists():
            raise serializers.ValidationError("У вас уже есть активная подписка.")

        plan = serializer.validated_data["plan"]
        start_date = now()
        end_date = start_date + timedelta(days=plan.duration_days)

        subscription = serializer.save(user=user, start_date=start_date, end_date=end_date)
        logger.info(f"Пользователь {user} оформил подписку {subscription.plan.name}")

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def extend(self, request, pk=None):
        """Продлить подписку"""
        subscription = self.get_object()

        if not subscription.is_active():
            return Response({"error": "Нельзя продлить истекшую подписку."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubscriptionExtendSerializer(data=request.data)
        if serializer.is_valid():
            extra_days = serializer.validated_data["extra_days"]

            if subscription.end_date + timedelta(days=extra_days) > now() + timedelta(days=365):
                return Response({"error": "Нельзя продлевать подписку более чем на 1 год."}, status=status.HTTP_400_BAD_REQUEST)

            subscription.end_date += timedelta(days=extra_days)
            subscription.save()
            return Response({"message": "Подписка продлена", "new_end_date": subscription.end_date},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_subscriptions(self, request):
        """Получить подписки текущего пользователя"""
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)
