from django.contrib import admin
from .models import *


admin.site.site_header = "Sistema de Gestão Educacional"
admin.site.site_title = "Administração"
admin.site.index_title = "SGE-GP"
admin.site.site_url = "/disciplinas"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_code']
    search_fields = ['name']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__', 'code']
    list_filter = ['academic_year', 'level']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'class_code', 'date']
    search_fields = ['subject__name']
    list_filter = ['date']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date']
    search_fields = ['school_test', 'subject__name', 'class_code']
    list_filter = ['date', 'school_test']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'grade']
    list_filter = ['test__date', 'test__school_test']
    search_fields = ['student', 'test']
    readonly_fields = ['student', 'test']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'delivery_date']
    search_fields = ['title', 'subject__name']
    readonly_fields = ['creation_date']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_time']
    search_fields = ['title']
    list_filter = ['date_time']