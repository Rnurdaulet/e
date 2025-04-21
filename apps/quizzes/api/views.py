from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import IsAdminOrContentManager, IsOwnerOrSchoolAdmin
from .serializers import (
    QuizSerializer, QuestionSerializer, AnswerSerializer, OrderingItemSerializer, MatchingPairSerializer,
    GroupSerializer, GroupItemSerializer, InputAnswerSerializer, SelectOptionSerializer, SelectOptionItemSerializer,
    UserAnswerSerializer, SubmitAnswerSerializer, UserQuizProgressSerializer, InputAnswerItemSerializer
)
from ..models import (
    Quiz, Question, Answer, OrderingItem, MatchingPair,
    Group, GroupItem, InputAnswer, SelectOption,
    UserAnswer, UserQuizProgress, InputAnswerItem, SelectOptionItem
)

User = get_user_model()


class QuizViewSet(viewsets.ModelViewSet):
    """API для тестов"""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]


class QuestionViewSet(viewsets.ModelViewSet):
    """API для вопросов"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["quiz"]  # quiz_id для фильтрации вопросов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "quiz",
                openapi.IN_QUERY,
                description="Фильтр вопросов по quiz_id",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AnswerViewSet(viewsets.ModelViewSet):
    """API для вариантов ответа"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderingItemViewSet(viewsets.ModelViewSet):
    """API для сортировки"""
    queryset = OrderingItem.objects.all()
    serializer_class = OrderingItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MatchingPairViewSet(viewsets.ModelViewSet):
    """API для соответствия"""
    queryset = MatchingPair.objects.all()
    serializer_class = MatchingPairSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    """API для групп"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GroupItemViewSet(viewsets.ModelViewSet):
    """API для элементов внутри групп"""
    queryset = GroupItem.objects.all()
    serializer_class = GroupItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]


class InputAnswerViewSet(viewsets.ModelViewSet):
    """API для текстовых ответов"""
    queryset = InputAnswer.objects.all()
    serializer_class = InputAnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class InputAnswerItemViewSet(viewsets.ModelViewSet):
    """API для текстовых ответов"""
    queryset = InputAnswerItem.objects.all()
    serializer_class = InputAnswerItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["inputAnswer"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "inputAnswer",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SelectOptionViewSet(viewsets.ModelViewSet):
    """API для выпадающего списка"""
    queryset = SelectOption.objects.all()
    serializer_class = SelectOptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
class SelectOptionItemViewSet(viewsets.ModelViewSet):
    """API для текстовых ответов"""
    queryset = SelectOptionItem.objects.all()
    serializer_class = SelectOptionItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrContentManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["selectOption"]  # question для фильтрации ответов

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "selectOption",
                openapi.IN_QUERY,
                description="Фильтр ответов по question",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class UserAnswerFilter(django_filters.FilterSet):
    """Фильтры для UserAnswer"""
    school = django_filters.NumberFilter(field_name="user__profile__school__id", lookup_expr="exact")
    school_class = django_filters.NumberFilter(field_name="user__profile__school_class__id", lookup_expr="exact")
    school_class_prefix = django_filters.NumberFilter(field_name="user__profile__school_class_prefix__id",
                                                      lookup_expr="exact")
    question = django_filters.NumberFilter(field_name="question__id", lookup_expr="exact")
    user = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    quiz = django_filters.NumberFilter(field_name="question__quiz__id", lookup_expr="exact")

    class Meta:
        model = UserAnswer
        fields = ["school", "school_class", "school_class_prefix", "question", "user", "quiz"]


class UserAnswerViewSet(viewsets.ModelViewSet):
    """Ответы пользователей"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSchoolAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAnswerFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("school", openapi.IN_QUERY, description="Фильтр по школе (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("school_class", openapi.IN_QUERY, description="Фильтр по классу (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("school_class_prefix", openapi.IN_QUERY, description="Фильтр по префиксу класса (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("question", openapi.IN_QUERY, description="Фильтр по вопросу (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("user", openapi.IN_QUERY, description="Фильтр по пользователю (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("quiz", openapi.IN_QUERY, description="Фильтр по тесту (ID)", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """Фильтруем ответы в зависимости от роли"""
        user = self.request.user

        if user.role == user.Role.ADMIN:
            return UserAnswer.objects.all()

        if user.role in [user.Role.EXPERT, user.Role.TEACHER, user.Role.SCHOOL_ADMIN]:
            return UserAnswer.objects.filter(user__school=user.school)

        return UserAnswer.objects.filter(user=user)

    def perform_create(self, serializer):
        """Запрещаем создавать ответ за другого пользователя"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request):
        """Отправка ответа пользователем"""
        serializer = SubmitAnswerSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            question = serializer.validated_data["question"]
            selected_answers = serializer.validated_data.get("selected_answers", [])
            input_text = serializer.validated_data.get("input_text", "").strip().lower()

            user_answer = UserAnswer.objects.create(
                user=user,
                question=question,
                input_text=input_text if question.question_type == "input" else None,
            )

            if question.question_type in ["single_choice", "multiple_choice"]:
                user_answer.selected_answers.set(selected_answers)
                correct_answers = set(question.answers.filter(is_correct=True))
                user_answer.is_correct = set(correct_answers) == set(selected_answers)

            elif question.question_type == "input":
                correct_texts = question.input_answers.first().correct_texts
                user_answer.is_correct = input_text in [t.lower() for t in correct_texts]

            user_answer.save()

            # Обновляем прогресс пользователя
            progress, created = UserQuizProgress.objects.get_or_create(user=user, quiz=question.quiz)
            progress.update_progress()

            return Response({"message": "Ответ принят", "is_correct": user_answer.is_correct},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserQuizProgressFilter(django_filters.FilterSet):
    """Фильтры для UserQuizProgress"""
    school = django_filters.NumberFilter(field_name="user__profile__school__id", lookup_expr="exact")
    school_class = django_filters.NumberFilter(field_name="user__profile__school_class__id", lookup_expr="exact")
    school_class_prefix = django_filters.NumberFilter(field_name="user__profile__school_class_prefix__id", lookup_expr="exact")
    user = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    quiz = django_filters.NumberFilter(field_name="quiz__id", lookup_expr="exact")

    class Meta:
        model = UserQuizProgress
        fields = ["school", "school_class", "school_class_prefix", "user", "quiz"]



class UserQuizProgressViewSet(viewsets.ModelViewSet):
    """Прогресс пользователя по тестам"""
    queryset = UserQuizProgress.objects.all()
    serializer_class = UserQuizProgressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSchoolAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserQuizProgressFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("school", openapi.IN_QUERY, description="Фильтр по школе (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("school_class", openapi.IN_QUERY, description="Фильтр по классу (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("school_class_prefix", openapi.IN_QUERY, description="Фильтр по префиксу класса (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("user", openapi.IN_QUERY, description="Фильтр по пользователю (ID)",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter("quiz", openapi.IN_QUERY, description="Фильтр по тесту (ID)", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """Фильтруем прогресс пользователей в зависимости от роли"""
        user = self.request.user

        if user.role == user.Role.ADMIN:
            return UserQuizProgress.objects.all()

        if user.role in [user.Role.EXPERT, user.Role.TEACHER, user.Role.SCHOOL_ADMIN]:
            return UserQuizProgress.objects.filter(user__school=user.school)

        return UserQuizProgress.objects.filter(user=user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_progress(self, request):
        """Возвращает прогресс текущего пользователя"""
        user_progress = UserQuizProgress.objects.filter(user=request.user)
        serializer = self.get_serializer(user_progress, many=True)
        return Response(serializer.data)
