from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from allauth.socialaccount.models import SocialAccount
from .models import CustomUser
from .models import StudentProfile, TeacherProfile


class CustomLoginForm(LoginForm):
    """Кастомизация формы входа"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Email"
        self.fields['password'].label = "Пароль"


class CustomSignupForm(SignupForm):
    """Кастомизация формы регистрации"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"


class UpdateNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Введите имя")}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Введите фамилию")}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Получаем пользователя
        super().__init__(*args, **kwargs)

        # Проверяем, авторизован ли пользователь через Microsoft
        if user and SocialAccount.objects.filter(user=user, provider="microsoft").exists():
            self.fields["first_name"].widget.attrs["readonly"] = True
            self.fields["last_name"].widget.attrs["readonly"] = True
            self.fields["first_name"].help_text = _("Вы вошли через Microsoft. Изменение имени запрещено.")
            self.fields["last_name"].help_text = _("Вы вошли через Microsoft. Изменение фамилии запрещено.")


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('school', 'school_class', 'school_class_prefix', 'language')


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ('school', 'language', 'subject')


class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',)
