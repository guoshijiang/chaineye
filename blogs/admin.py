#encoding=utf-8


from django.contrib import admin
from blogs.models import Tag, Article, ChainSafe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'user', 'views', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(ChainSafe)
class ChainSafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')



