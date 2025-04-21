from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from .models import (
    Quiz, Question, Answer, OrderingItem, MatchingPair, Group, GroupItem,
    InputAnswer, SelectOption, UserAnswer, UserQuizProgress, InputAnswerItem, SelectOptionItem
)


class QuestionInline(StackedInline):
    """Отображение элементов группы в админке внутри группы"""
    model = Question
    extra = 0  # Количество пустых полей для добавления новых элементов
    show_change_link = True  # Позволяет редактировать объект


@admin.register(Quiz)
class QuizAdmin(ModelAdmin):
    """Админка для тестов"""
    list_display = ("title", "created_at")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    """Админка для вопросов"""
    list_display = ("text", "quiz", "question_type")
    list_filter = ("question_type",)
    search_fields = ("text", "quiz__title")
    autocomplete_fields = ("quiz",)


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    """Админка для вариантов ответа"""
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text", "question__text")
    autocomplete_fields = ("question",)


@admin.register(OrderingItem)
class OrderingItemAdmin(ModelAdmin):
    """Админка для элементов сортировки"""
    list_display = ("text", "question", "order")
    search_fields = ("text", "question__text")
    autocomplete_fields = ("question",)


@admin.register(MatchingPair)
class MatchingPairAdmin(ModelAdmin):
    """Админка для соответствий"""
    list_display = ("left_side", "right_side", "question")
    search_fields = ("left_side", "right_side", "question__text")
    autocomplete_fields = ("question",)


class GroupItemInline(StackedInline):
    """Отображение элементов группы в админке внутри группы"""
    model = GroupItem
    extra = 0  # Количество пустых полей для добавления новых элементов
    show_change_link = True  # Позволяет редактировать объект


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    """Админка для групп"""
    list_display = ("name", "question")
    search_fields = ("name", "question__text")
    autocomplete_fields = ("question",)
    inlines = [GroupItemInline]


@admin.register(GroupItem)
class GroupItemAdmin(ModelAdmin):
    """Админка для элементов в группах"""
    list_display = ("text", "group__name")
    search_fields = ("text", "group__name")
    autocomplete_fields = ("group",)


class InputAnswerItemInline(StackedInline):
    """Отображение элементов группы в админке внутри группы"""
    model = InputAnswerItem
    extra = 0  # Количество пустых полей для добавления новых элементов
    show_change_link = True  # Позволяет редактировать объект



@admin.register(InputAnswer)
class InputAnswerAdmin(ModelAdmin):
    """Админка для правильных текстовых ответов"""
    list_display = ("id","question",)
    search_fields = ("question__text","text")
    autocomplete_fields = ("question",)
    inlines = [InputAnswerItemInline]


@admin.register(InputAnswerItem)
class InputAnswerItemAdmin(ModelAdmin):
    """Админка для правильных текстовых ответов"""
    list_display = ("number", "input_placeholder")
    search_fields = ("number", "input_placeholder", "input_correct_text")
    autocomplete_fields = ("inputAnswer",)

class SelectOptionItemInline(StackedInline):
    """Отображение элементов группы в админке внутри группы"""
    model = SelectOptionItem
    extra = 0  # Количество пустых полей для добавления новых элементов
    show_change_link = True  # Позволяет редактировать объект
@admin.register(SelectOption)
class SelectOptionAdmin(ModelAdmin):
    """Админка для вариантов выпадающего списка"""
    list_display = ("id","question",)
    search_fields = ("question__text","text")
    autocomplete_fields = ("question",)
    inlines = [SelectOptionItemInline]
@admin.register(SelectOptionItem)
class SelectOptionItemAdmin(ModelAdmin):
    """Админка для правильных текстовых ответов"""
    list_display = ("number", "select_placeholder")
    search_fields = ("number", "select_placeholder", "select_correct_text", "select_option_text")
    autocomplete_fields = ("selectOption",)
@admin.register(UserAnswer)
class UserAnswerAdmin(ModelAdmin):
    """Админка для ответов пользователей"""
    list_display = ("user", "question", "is_correct", "answered_at")
    list_filter = ("is_correct", "answered_at")
    search_fields = ("user__username", "question__text")
    autocomplete_fields = ("user", "question", "selected_option")
    date_hierarchy = "answered_at"
    readonly_fields = ("answered_at",)
    fieldsets = (
        (None, {"fields": ("user", "question", "is_correct", "answered_at")}),
        ("Выбор", {"fields": ("selected_answers", "selected_option")}),
        ("Свободный ввод", {"fields": ("input_text",)}),
        ("Дополнительные данные", {"fields": ("selected_order", "selected_matching", "selected_grouping")}),
    )


@admin.register(UserQuizProgress)
class UserQuizProgressAdmin(ModelAdmin):
    """Админка для прогресса пользователей в тестах"""
    list_display = ("user", "quiz", "score_percentage", "answered_questions", "total_questions", "completed_at")
    list_filter = ("completed_at",)
    search_fields = ("user__username", "quiz__title")
    autocomplete_fields = ("user", "quiz")
    readonly_fields = ("answered_questions", "correct_answers", "score_percentage", "completed_at")

    fieldsets = (
        (None, {"fields": ("user", "quiz")}),
        ("Прогресс", {"fields": ("answered_questions", "correct_answers", "total_questions", "score_percentage")}),
        ("Завершение", {"fields": ("completed_at",)}),
    )
