from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/<int:pk>/extend/', SubscriptionViewSet.as_view({'post': 'extend'}), name="subscription-extend"),
    path('subscriptions/my/', SubscriptionViewSet.as_view({'get': 'my_subscriptions'}), name="my-subscriptions"),
]
