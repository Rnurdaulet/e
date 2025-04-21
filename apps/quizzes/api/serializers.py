from rest_framework import serializers
from ..models import (
    Quiz, Question, Answer, OrderingItem, MatchingPair,
    Group, GroupItem, InputAnswer, InputAnswerItem, SelectOption, SelectOptionItem,
    UserAnswer, UserQuizProgress
)


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для вариантов ответа (Single Choice, Multiple Choice)"""

    class Meta:
        model = Answer
        fields = ["id", "question", "text", "is_correct"]


class OrderingItemSerializer(serializers.ModelSerializer):
    """Сериализатор для сортировки (Ordering)"""

    class Meta:
        model = OrderingItem
        fields = ["id", "question", "text", "order"]


class MatchingPairSerializer(serializers.ModelSerializer):
    """Сериализатор для соответствия (Matching)"""

    class Meta:
        model = MatchingPair
        fields = ["id", "question", "left_side", "right_side"]


class GroupItemSerializer(serializers.ModelSerializer):
    """Сериализатор для элементов внутри групп (Grouping)"""

    class Meta:
        model = GroupItem
        fields = ["id", "group", "text"]


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп (Grouping)"""
    items = GroupItemSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "question", "name", "items"]


class InputAnswerItemSerializer(serializers.ModelSerializer):
    """Сериализатор для текстовых ответов (Input)"""
    input_correct_text = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    class Meta:
        model = InputAnswerItem
        fields = ["id", "number", "input_placeholder", "input_correct_text"]


class InputAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для текстовых ответов (Input)"""
    input_answer = InputAnswerItemSerializer(many=True, read_only=True)

    class Meta:
        model = InputAnswer
        fields = ["id", "question", "text", "input_answer"]

class SelectOptionItemSerializer(serializers.ModelSerializer):
    """Сериализатор для текстовых ответов (Input)"""
    select_option_text = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    class Meta:
        model = SelectOptionItem
        fields = ["id", "number", "select_placeholder", "select_correct_text", "select_option_text"]

class SelectOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для выпадающего списка (Select)"""
    select_option = SelectOptionItemSerializer(many=True, read_only=True)
    class Meta:
        model = SelectOption
        fields = ["id", "question", "text", "select_option"]


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""
    answers = AnswerSerializer(many=True, read_only=True)
    ordering_items = OrderingItemSerializer(many=True, read_only=True)
    matching_pairs = MatchingPairSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    input_answers = InputAnswerSerializer(many=True, read_only=True)
    select_options = SelectOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "quiz", "text", "question_type", "answers", "ordering_items",
                  "matching_pairs", "groups", "input_answers", "select_options"]


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для тестов"""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at", "questions"]


class UserAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответов пользователей"""

    class Meta:
        model = UserAnswer
        fields = ["id", "user", "question", "selected_answers", "input_text",
                  "selected_order", "selected_matching", "selected_grouping",
                  "selected_option", "is_correct", "answered_at"]


class SubmitAnswerSerializer(serializers.Serializer):
    """Сериализатор для отправки ответа на вопрос"""
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    selected_answers = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), many=True, required=False)
    input_text = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    selected_order = serializers.ListField(child=serializers.IntegerField(), required=False)
    selected_matching = serializers.ListField(child=serializers.JSONField(), required=False)
    selected_grouping = serializers.ListField(child=serializers.JSONField(), required=False)
    selected_option = serializers.PrimaryKeyRelatedField(queryset=SelectOption.objects.all(), required=False,
                                                         allow_null=True)


class UserQuizProgressSerializer(serializers.ModelSerializer):
    """Сериализатор для прогресса пользователей"""

    class Meta:
        model = UserQuizProgress
        fields = ["id", "user", "quiz", "total_questions",
                  "answered_questions", "correct_answers",
                  "score_percentage", "completed_at"]
