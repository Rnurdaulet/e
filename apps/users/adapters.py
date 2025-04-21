from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyMicrosoftAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Разрешаем автоматическую регистрацию пользователей,
        если они входят через Microsoft AD.
        """
        if sociallogin.account.provider == "microsoft":
            return True  # Не требуем подтверждение email
        return super().is_auto_signup_allowed(request, sociallogin)
