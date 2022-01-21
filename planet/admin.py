#encoding=utf-8

from django.contrib import admin
from planet.models import (
   CourseCat, Course, CourseArtcle, CourseCommet
)


@admin.register(CourseCat)
class CourseCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(CourseArtcle)
class CourseArtcleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(CourseCommet)
class CourseCommetAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'content')
