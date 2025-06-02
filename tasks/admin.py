from django.contrib import admin
from .models import Column, Task, Discipline, GradeLevel, Activity

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'discipline', 'grade_level', 'column', 'assignee', 'updated_at')
    list_filter = ('column', 'assignee', 'discipline', 'grade_level')
    search_fields = ('title', 'discipline__name', 'grade_level__name', 'description')


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)