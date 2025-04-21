from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TextbookViewSet, IntroductionViewSet, SectionViewSet, LessonViewSet, KeywordViewSet

router = DefaultRouter()
router.register(r'textbooks', TextbookViewSet, basename='textbook')
router.register(r'introductions', IntroductionViewSet, basename='introduction')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'keywords', KeywordViewSet, basename='keyword')

urlpatterns = [
    path('', include(router.urls)),
]
