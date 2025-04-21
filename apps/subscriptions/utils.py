from django.utils.timezone import now
from .models import Subscription

def user_has_access(user):
    """ Проверяет, есть ли у пользователя активная подписка (персональная или корпоративная) """
    personal_subscription = Subscription.objects.filter(user=user, end_date__gte=now()).first()

    if personal_subscription:
        return True

    if hasattr(user, "school"):  # Если у пользователя есть школа
        corporate_subscription = Subscription.objects.filter(school=user.school, end_date__gte=now()).first()
        return corporate_subscription is not None

    return False
