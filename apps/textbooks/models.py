from django.db import models
from apps.education.models import Subject, SchoolClass, Language
from apps.quizzes.models import Quiz
from apps.subscriptions.models import Plan


class Textbook(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="textbooks")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="textbooks")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="textbooks")
    isbn = models.CharField(max_length=17, unique=True, verbose_name="ISBN")
    title = models.CharField(max_length=255, verbose_name="Название учебника")
    required_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="Требуемый план")
    image = models.ImageField(upload_to="textbooks/", blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return f"{self.title} ({self.language})"


class Introduction(models.Model):
    textbook = models.OneToOneField(Textbook, on_delete=models.CASCADE, related_name="introduction")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="textbooks/introductions/", blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return f"Введение для {self.textbook.title}"


class Section(models.Model):
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255, verbose_name="Название раздела")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="textbooks/sections/", blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return f"{self.title} ({self.textbook.title})"


class Keyword(models.Model):
    text = models.CharField(max_length=100, unique=True, verbose_name="Текст")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.text


class Lesson(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255, verbose_name="Тема урока")
    objective = models.TextField(verbose_name="Цель урока")
    description = models.TextField(verbose_name="Описание")
    keywords = models.ManyToManyField(Keyword, blank=True, related_name="lessons", verbose_name="Ключевые слова")
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тест")

    def __str__(self):
        return f"{self.title} ({self.section.title})"
