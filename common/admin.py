#encoding=utf-8

from django.contrib import admin
from common.models import (
    Banner, Category, Advertise, Partner, Asset
)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')


@admin.register(Advertise)
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Partner)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','link_url')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')



