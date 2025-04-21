from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TranslationAdmin
from .models import Region, City, School, SchoolClass, Language, Subject, SchoolClassPrefix


@admin.register(Region)
class RegionAdmin(TranslationAdmin,ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(TranslationAdmin,ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)


@admin.register(School)
class SchoolAdmin(TranslationAdmin,ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(TranslationAdmin,ModelAdmin):
    list_display = ('name',)


@admin.register(SchoolClass)
class SchoolClassAdmin(ModelAdmin):
    list_display = ('grade',)
    list_filter = ('grade', )
    search_fields = ('grade',)


@admin.register(SchoolClassPrefix)
class SchoolClassPrefixAdmin(ModelAdmin):
    list_display = ("prefix",)
    search_fields = ("prefix",)
    ordering = ("prefix",)


@admin.register(Subject)
class SubjectAdmin(TranslationAdmin,ModelAdmin):
    list_display = ('name',)
