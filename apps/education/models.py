from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Область"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Область")
        verbose_name_plural = _("Области")


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Город"))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name} ({self.region.name})"

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")


class School(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Школа"))
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="schools")

    def __str__(self):
        return f"{self.name}, {self.city.name}"

    class Meta:
        verbose_name = _("Школа")
        verbose_name_plural = _("Школы")


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Язык обучения"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Язык обучения")
        verbose_name_plural = _("Языки обучения")


class SchoolClass(models.Model):
    GRADE_CHOICES = [(i, f"{i}") for i in range(1, 13)]  # Классы от 7 до 12

    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, verbose_name=_("Класс"))

    def __str__(self):
        return f"{self.grade}"

    class Meta:
        verbose_name = _("Класс")
        verbose_name_plural = _("Классы")


class SchoolClassPrefix(models.Model):
    """Префиксы классов (А, Ә, Б, В, Г, Ғ и т. д.)"""
    PREFIX_CHOICES = [
        ("А", "А"),
        ("Ә", "Ә"),
        ("Б", "Б"),
        ("В", "В"),
        ("Г", "Г"),
        ("Ғ", "Ғ"),
        ("Д", "Д"),
        ("Е", "Е"),
        ("Ё", "Ё"),
        ("Ж", "Ж"),
        ("З", "З"),
    ]

    prefix = models.CharField(max_length=1, choices=PREFIX_CHOICES, unique=True, verbose_name=_("Префикс"))

    def __str__(self):
        return self.prefix

    class Meta:
        verbose_name = _("Префикс класса")
        verbose_name_plural = _("Префиксы классов")


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название предмета"))
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Код предмета"))  # Добавляем поле code

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")
