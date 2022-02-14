#encoding=utf-8

from django.contrib import admin
from ceye_auth.models import Account, User, UserInfo, UserBuyCourse


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'phone')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'user_name')


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'real_name', 'sex')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'real_name')


@admin.register(UserBuyCourse)
class UserBuyCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_id')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'course_id')