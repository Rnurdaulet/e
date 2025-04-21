from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from ..models import Region, City, School, Language, SchoolClass, SchoolClassPrefix, Subject
from .serializers import (
    RegionSerializer, CitySerializer, SchoolSerializer, LanguageSerializer,
    SchoolClassSerializer, SchoolClassPrefixSerializer, SubjectSerializer
)


class RegionViewSet(viewsets.ModelViewSet):
    """API для регионов"""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    """API для городов"""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["region"]


class SchoolViewSet(viewsets.ModelViewSet):
    """API для школ"""
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["city"]


class LanguageViewSet(viewsets.ModelViewSet):
    """API для языков обучения"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class SchoolClassViewSet(viewsets.ModelViewSet):
    """API для классов"""
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class SchoolClassPrefixViewSet(viewsets.ModelViewSet):
    """API для префиксов классов"""
    queryset = SchoolClassPrefix.objects.all()
    serializer_class = SchoolClassPrefixSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    """API для предметов"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
