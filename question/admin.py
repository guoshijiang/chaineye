#encoding=utf-8

from django.contrib import admin
from question.models import (
    Questions, Answers
)


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'content')

