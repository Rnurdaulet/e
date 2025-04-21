from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils import timezone


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "single_choice", "Single Choice"
    MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
    ORDERING = "ordering", "Ordering"
    MATCHING = "matching", "Matching"
    GROUPING = "grouping", "Grouping"
    INPUT = "input", "Input"
    SELECT = "select", "Select"


class Quiz(models.Model):
    """Тест, содержащий вопросы"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопрос, принадлежащий тесту"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QuestionType.choices)

    class Meta:
        ordering = ["quiz", "id"]

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Вариант ответа для Single и Multiple Choice"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class OrderingItem(models.Model):
    """Элемент для сортировки (Ordering)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="ordering_items")
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ("question", "order")  # Запрещает дубли порядковых номеров


class MatchingPair(models.Model):
    """Соответствие (Matching)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="matching_pairs")
    left_side = models.CharField(max_length=255)
    right_side = models.CharField(max_length=255)

    class Meta:
        unique_together = ("question", "left_side", "right_side")  # Исключает дубликаты


class Group(models.Model):
    """Группа для группировки (Grouping)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GroupItem(models.Model):
    """Элемент внутри группы (Grouping)"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="items")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class InputAnswer(models.Model):
    """Правильный текстовый ответ (Input)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="input_answers")
    text = models.TextField()

    class Meta:
        ordering = ["id"]
    def __str__(self):
        return self.text


class InputAnswerItem(models.Model):
    """Правильный текстовый ответ (Input)"""
    inputAnswer = models.ForeignKey(InputAnswer, on_delete=models.CASCADE, related_name="input_answer")
    number = models.IntegerField(default=0)
    input_placeholder = models.CharField(max_length=255, blank=True, null=True)
    # input_correct_text = models.TextField(blank=True, null=True)
    input_correct_text = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
        null=True
    )
    class Meta:
        ordering = ["id"]
    def __str__(self):
        return self.input_placeholder


class SelectOption(models.Model):
    """Варианты ответа для выпадающего списка (Select)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="select_options")
    text = models.TextField()

    class Meta:
        ordering = ["id"]
    def __str__(self):
        return self.text

class SelectOptionItem(models.Model):
    """Правильный текстовый ответ (Input)"""
    selectOption = models.ForeignKey(SelectOption, on_delete=models.CASCADE, related_name="select_option")
    number = models.IntegerField(default=0)
    select_placeholder = models.CharField(max_length=255, blank=True, null=True)
    select_correct_text = models.TextField(blank=True, null=True)
    select_option_text = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
        null=True
    )
    class Meta:
        ordering = ["id"]
    def __str__(self):
        return self.select_placeholder
class UserAnswer(models.Model):
    """Ответ пользователя на вопрос"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_answers")
    selected_answers = models.ManyToManyField(Answer, blank=True)  # Для Single и Multiple Choice
    input_text = models.CharField(max_length=255, blank=True, null=True)  # Для Input
    selected_order = ArrayField(models.PositiveIntegerField(), blank=True, null=True)  # Для Ordering
    selected_matching = ArrayField(models.JSONField(), blank=True, null=True)  # Для Matching (хранение пар)
    selected_grouping = ArrayField(models.JSONField(), blank=True, null=True)  # Для Grouping (группы и элементы)
    selected_option = models.ForeignKey(SelectOption, on_delete=models.SET_NULL, blank=True, null=True)  # Для Select
    is_correct = models.BooleanField(default=False)  # Верный ли ответ
    answered_at = models.DateTimeField(auto_now_add=True)  # Дата и время ответа

    class Meta:
        ordering = ["-answered_at"]

    def __str__(self):
        return f"{self.user} → {self.question} ({'✔' if self.is_correct else '✘'})"


class UserQuizProgress(models.Model):
    """Прогресс пользователя в тесте"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="quiz_progress")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="user_progress")
    total_questions = models.PositiveIntegerField(default=0)
    answered_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    score_percentage = models.FloatField(default=0.0)  # Процент правильных ответов
    completed_at = models.DateTimeField(blank=True, null=True)  # Когда тест завершен

    class Meta:
        ordering = ["-completed_at"]

    def update_progress(self):
        """Обновляет статистику прохождения теста"""
        self.answered_questions = UserAnswer.objects.filter(user=self.user, question__quiz=self.quiz).count()
        self.correct_answers = UserAnswer.objects.filter(user=self.user, question__quiz=self.quiz,
                                                         is_correct=True).count()
        self.total_questions = self.quiz.questions.count()
        self.score_percentage = (self.correct_answers / self.total_questions) * 100 if self.total_questions else 0
        if self.answered_questions == self.total_questions:
            self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user} - {self.quiz} ({self.score_percentage:.2f}%)"
