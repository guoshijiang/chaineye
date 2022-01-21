#encoding=utf-8

from django.contrib import admin
from activity.models import (
    Area, Activity, PartActivity, SponsorActivity, CoinAddress
)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'company', 'author', 'views', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(PartActivity)
class PartActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'company', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'username')


@admin.register(SponsorActivity)
class SponsorActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'name')


@admin.register(CoinAddress)
class CoinAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin', 'address', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'coin')