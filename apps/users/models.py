import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from PIL import Image
from apps.education.models import SchoolClass, SchoolClassPrefix, Language, School, Subject


def validate_avatar_size(image):
    max_size = 1 * 1024 * 1024  # 1 МБ
    if image.size > max_size:
        raise ValidationError(_("Размер файла не должен превышать 1 МБ."))


def validate_image_extension(image):
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(_("Недопустимый формат изображения. Допустимые форматы: JPG, JPEG, PNG, GIF."))


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        extra_fields.setdefault("is_active", True)

        # Используем self.model.Role вместо Role
        role = role or self.model.Role.USER

        user = self.model(email=self.normalize_email(email), role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Автоматическое добавление в соответствующую группу
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("has_full_access", True)
        return self.create_user(email, password, role="admin", **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        USER = "user", _("Пользователь")
        CONTENT_MANAGER = "content_manager", _("Контент-менеджер")
        SCHOOL_ADMIN = "school_admin", _("Администратор школы")
        EXPERT = "expert", _("Эксперт")  # Смесь Учитель + Школьник
        STUDENT = "student", _("Школьник")
        TEACHER = "teacher", _("Учитель")
        ADMIN = "admin", _("Администратор")

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.STUDENT, verbose_name=_("Роль"))

    iin = models.CharField(
        max_length=12,
        # unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^\d{12}$", _("ИИН должен содержать 12 цифр"))],
        verbose_name=_("ИИН"),
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^\+?[1-9]\d{1,14}$", _("Некорректный формат телефона"))],
        verbose_name=_("Телефон"),
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    has_full_access = models.BooleanField(default=False, verbose_name=_("Полный доступ"))

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[validate_avatar_size, validate_image_extension],
        verbose_name=_("Аватар"),
    )

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата изменения"))

    history = HistoricalRecords()
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        indexes = [models.Index(fields=["first_name", "iin"])]
        constraints = [models.UniqueConstraint(fields=["email"], name="unique_email")]

    def get_full_name(self):
        """Возвращает полное имя пользователя (имя + фамилия)"""
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.thumbnail((300, 300))
                img.save(self.avatar.path, optimize=True, quality=85)
            except Exception:
                pass


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")

    # Общие поля
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True, related_name="users", verbose_name=_("Школа")
    )
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True, related_name="users",
        verbose_name=_("Язык обучения")
    )

    # Поля только для студентов
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, related_name="students", verbose_name=_("Класс")
    )
    school_class_prefix = models.ForeignKey(
        SchoolClassPrefix, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Префикс класса")
    )

    # Поля только для учителей
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="teachers", verbose_name=_("Предмет")
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.get_role_display()})"



