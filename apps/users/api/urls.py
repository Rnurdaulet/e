from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, CustomLoginView, RegisterView
from dj_rest_auth.views import (PasswordChangeView,
                                PasswordResetView, PasswordResetConfirmView, LogoutView
                                )

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("auth/password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path("auth/password/reset/confirm/", PasswordResetConfirmView.as_view(), name="rest_password_reset_confirm"),
    path('', include(router.urls)),
]
