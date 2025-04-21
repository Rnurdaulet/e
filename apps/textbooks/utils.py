from django.utils.timezone import now
from django.db import models
from apps.subscriptions.models import Subscription

def user_can_access_textbook(user, textbook):
    """ Проверяет, может ли пользователь получить доступ к учебнику """
    if textbook.required_plan is None:
        return True  # Учебник бесплатный

    subscription = Subscription.objects.filter(
        models.Q(user=user) | models.Q(school=user.school),
        end_date__gte=now()
    ).first()

    return subscription and subscription.plan.id == textbook.required_plan.id
