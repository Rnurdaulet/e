from rest_framework import serializers
from ..models import Region, City, School, Language, SchoolClass, SchoolClassPrefix, Subject


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для регионов"""

    class Meta:
        model = Region
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для городов"""

    class Meta:
        model = City
        fields = ["id", "name", "region"]


class SchoolSerializer(serializers.ModelSerializer):
    """Сериализатор для школ"""

    class Meta:
        model = School
        fields = ["id", "name", "city"]


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализатор для языков обучения"""

    class Meta:
        model = Language
        fields = ["id", "name"]


class SchoolClassSerializer(serializers.ModelSerializer):
    """Сериализатор для классов"""

    class Meta:
        model = SchoolClass
        fields = ["id", "grade"]


class SchoolClassPrefixSerializer(serializers.ModelSerializer):
    """Сериализатор для префиксов классов"""

    class Meta:
        model = SchoolClassPrefix
        fields = ["id", "prefix"]


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов"""

    class Meta:
        model = Subject
        fields = ["id", "name", "code"]
