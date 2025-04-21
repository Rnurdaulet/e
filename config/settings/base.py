import logging
import os
import sys
from pathlib import Path
from decouple import config
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.template.context_processors import static

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = config("DEBUG", default="False")
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key')

INSTALLED_APPS = [
    'modeltranslation',

    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.simple_history",

    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',


    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',

    'simple_history',
    'import_export',
    'django_celery_beat',
    'widget_tweaks',
    'drf_yasg',
    'django_filters',

    'apps.users',
    'apps.education',
    'apps.quizzes',
    'apps.textbooks',
    'apps.subscriptions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # Добавляем в начало
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

######################################################################
# AUTH
######################################################################

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Стандартная аутентификация
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5501"
]

CORS_ALLOW_CREDENTIALS = True

######################################################################
# DRF
######################################################################

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'JWT_AUTH_HTTPONLY': True,
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'apps.users.serializers.CustomRegisterSerializer',
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.users.authentication.JWTCookieAuthentication",  # Добавляем поддержку cookie
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Для браузера
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 дней
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_SECURE = True  # Обязательно, если используешь HTTPS
SESSION_COOKIE_SECURE = True  # Для HTTPS
JWT_AUTH_SECURE = True  # Включает secure cookies

# APPEND_SLASH = False
######################################################################
# JWT
######################################################################

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": config('SECRET_KEY', default='django-insecure-default-key'),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
}

######################################################################
# Time
######################################################################

TIME_ZONE = 'Asia/Aqtobe'
USE_TZ = True

######################################################################
# Static & Media
######################################################################

# Настройка статики и медиа-файлов
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

######################################################################
# LOGIN
######################################################################


AUTH_USER_MODEL = 'users.CustomUser'  # Указываем кастомную модель пользователя

SITE_ID = 1  # Django требует для allauth

LOGIN_REDIRECT_URL = '/'  # Куда перенаправлять после входа
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'  # Куда после выхода

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False  # Отключаем username
ACCOUNT_LOGIN_METHODS = {'email'}  # Новый формат # Вход по email
ACCOUNT_EMAIL_REQUIRED = True  # Email обязателен
ACCOUNT_SIGNUP_REDIRECT_URL = '/'  # Куда перенаправлять после регистрации

ACCOUNT_EMAIL_VERIFICATION = "optional"  # Отключает обязательное подтверждение email
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # Отключает подтверждение email только для соц. входа
# URL для подтверждения email
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # Подтверждение по клику на ссылку
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Срок жизни ссылки

ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"

ACCOUNT_FORMS = {
    'login': 'apps.users.forms.CustomLoginForm',
    'signup': 'apps.users.forms.CustomSignupForm',
}
SOCIALACCOUNT_ADAPTER = "apps.users.adapters.MyMicrosoftAccountAdapter"

######################################################################
# EMAIL
######################################################################

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.kz"  # Gmail (используй smtp.yandex.ru или smtp.mail.ru, если Yandex или Mail.ru)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "oin@oin.kz"  # Твой email
EMAIL_HOST_PASSWORD = "imonctyxhviuzghs"  # Пароль приложения (НЕ обычный пароль!)
DEFAULT_FROM_EMAIL = "oin@oin.kz"

######################################################################
# LANGUAGES
######################################################################

LANGUAGE_CODE = 'ru'
USE_I18N = True

LANGUAGES = [
    ('ru', _('Русский')),
    ('kk', _('Қазақша')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LANGUAGE_COOKIE_NAME = 'language'
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 30

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_LANGUAGES = ('ru', 'kk', 'en')

######################################################################
# Unfold
######################################################################
#
UNFOLD = {
    "SITE_HEADER": "E-OQULYQ",
    "SITE_TITLE": "E-OQULYQ",
    "SITE_SYMBOL": "auto_stories",
    "SHOW_LANGUAGES": True,
    "SHOW_HISTORY": True,
    # "ENVIRONMENT": "utils.permissions.environment_callback",
    "LOGIN": {
        "image": lambda request: static("site/images/bg.svg"),
    }
}

######################################################################
# LOGGING
######################################################################

# import sentry_sdk
#
# sentry_sdk.init(
#     dsn="https://59c8227060925eef5862200b2811f142@o4508773889212416.ingest.de.sentry.io/4508773892292688",
#     send_default_pii=True,
#     traces_sample_rate=0.4,
#     environment="production-backend",
#     release="backend@1.0.0",
#     _experiments={
#         "continuous_profiling_auto_start": True,
#     },
# )


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'sentry': {
#             'level': 'ERROR',
#             'class': 'sentry_sdk.integrations.logging.EventHandler',
#         },
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['sentry', 'console'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }
