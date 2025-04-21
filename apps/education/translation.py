from modeltranslation.translator import register, TranslationOptions
from .models import Region, City, School, Language, SchoolClass, Subject


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(School)
class SchoolTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ('name',)
