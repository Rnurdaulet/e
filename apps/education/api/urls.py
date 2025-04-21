from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet, CityViewSet, SchoolViewSet, LanguageViewSet,
    SchoolClassViewSet, SchoolClassPrefixViewSet, SubjectViewSet
)

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'school-classes', SchoolClassViewSet, basename='school-class')
router.register(r'school-class-prefixes', SchoolClassPrefixViewSet, basename='school-class-prefix')
router.register(r'subjects', SubjectViewSet, basename='subject')

urlpatterns = [
    path('', include(router.urls)),
]
