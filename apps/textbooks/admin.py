from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import Textbook, Introduction, Section, Lesson, Keyword


@admin.register(Textbook)
class TextbookAdmin(ModelAdmin):
    list_display = ("title", "subject", "school_class", "language", "isbn")
    search_fields = ("title", "isbn")
    list_filter = ("subject", "school_class", "language")
    fieldsets = (
        (None, {"fields": ("title", "isbn")}),
        ("Связи", {"fields": ("subject", "school_class", "language")}),
        ("Подписка", {"fields": ("required_plan",)}),
    )


@admin.register(Introduction)
class IntroductionAdmin(ModelAdmin):
    list_display = ("textbook",)
    formfield_overrides = {
        "text": {"widget": WysiwygWidget(attrs={"rows": 5})},
    }


@admin.register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ("title", "textbook")
    search_fields = ("title",)
    list_filter = ("textbook",)
    formfield_overrides = {
        "text": {"widget": WysiwygWidget(attrs={"rows": 5})},
    }


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ("title", "section", "quiz")
    search_fields = ("title",)
    list_filter = ("section",)
    formfield_overrides = {
        "objective": {"widget": WysiwygWidget(attrs={"rows": 3})},
        "description": {"widget": WysiwygWidget(attrs={"rows": 5})},
    }
    filter_horizontal = ("keywords",)  # Удобный выбор ключевых слов в ManyToMany


@admin.register(Keyword)
class KeywordAdmin(ModelAdmin):
    list_display = ("text",)
    search_fields = ("text",)
    formfield_overrides = {
        "description": {"widget": WysiwygWidget(attrs={"rows": 3})},
    }
