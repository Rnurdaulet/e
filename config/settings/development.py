from decouple import config
from .base import *

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
INTERNAL_IPS = [
    "127.0.0.1",
]


# if DEBUG:  # Debug Toolbar только при DEBUG=True
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# STATIC_URL = "/static/"
# STATIC_ROOT = "/static/"
# STATICFILES_DIRS = [BASE_DIR / "static"]


# # Настройки Celery
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # URL брокера сообщений
# CELERY_ACCEPT_CONTENT = ['json']  # Формат данных
# CELERY_TASK_SERIALIZER = 'json'  # Сериализация задач
#
# # Настройки периодических задач через Django-Celery-Beat
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',  # Адрес и порт вашего Redis-сервера
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'KEY_PREFIX': 'nislab',  # Префикс для ключей в Redis
#     }
# }
