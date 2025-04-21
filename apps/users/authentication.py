from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

class JWTCookieAuthentication(JWTAuthentication):
    """Аутентификация через JWT-токены, хранящиеся в cookies"""

    def authenticate(self, request):
        # Получаем токены из cookies
        access_token = request.COOKIES.get(settings.REST_AUTH.get("JWT_AUTH_COOKIE"))
        refresh_token = request.COOKIES.get(settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"))

        # Если нет access-токена, но есть refresh-токен → создаем новый access
        if not access_token and refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)  # Генерируем новый access
                # Записываем новый access-токен в cookies (через response в middleware или в представлении)
                request.new_access_token = access_token
            except Exception:
                return None  # Refresh токен недействителен

        if not access_token:
            return None  # Нет токенов = нет аутентификации

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token
