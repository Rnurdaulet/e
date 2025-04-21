from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Main API",
        default_version="v1",
        description="Общая документация API",
        contact=openapi.Contact(email="support@yourdomain.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # API Токены
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Подключаем API пользователей
    path('api/v1/', include('apps.users.api.urls')),

    # API для образования
    path('api/v1/education/', include('apps.education.api.urls')),

    # API для викторин
    path('api/v1/quizzes/', include('apps.quizzes.api.urls')),

    # Подключение API учебников
    path('api/v1/textbooks/', include('apps.textbooks.api.urls')),

    # Подключение API подписок
    path('api/v1/subscriptions/', include('apps.subscriptions.api.urls')),

    # Основной Swagger (включает все)
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),

    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)
