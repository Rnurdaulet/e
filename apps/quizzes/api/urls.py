from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet, QuestionViewSet, AnswerViewSet, OrderingItemViewSet, MatchingPairViewSet,
    GroupViewSet, GroupItemViewSet, InputAnswerViewSet,InputAnswerItemViewSet, SelectOptionViewSet, SelectOptionItemViewSet,
    UserAnswerViewSet, UserQuizProgressViewSet
)

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'ordering-items', OrderingItemViewSet, basename='ordering-item')
router.register(r'matching-pairs', MatchingPairViewSet, basename='matching-pair')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'group-items', GroupItemViewSet, basename='group-item')
router.register(r'input-answers', InputAnswerViewSet, basename='input-answer')
router.register(r'input-answers-item', InputAnswerItemViewSet, basename='input-answer-item')
router.register(r'select-options', SelectOptionViewSet, basename='select-option')
router.register(r'select-options', SelectOptionItemViewSet, basename='select-option-item')
router.register(r'user-answers', UserAnswerViewSet, basename='user-answer')
router.register(r'user-progress', UserQuizProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),
    path('user-answers/submit/', UserAnswerViewSet.as_view({'post': 'submit'}), name="submit-answer"),
    path('user-progress/my/', UserQuizProgressViewSet.as_view({'get': 'my_progress'}), name="my-progress"),
]
