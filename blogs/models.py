#encoding=utf-8

from django.db import models
from DjangoUeditor.models import UEditorField
from common.models import BaseModel, Category
from ceye_auth.models import User
from mdeditor.fields import MDTextField


ANSWER_STATUS = [(x, x) for x in ['UnAnswer', 'Answered', 'Unknown']]


class Tag(BaseModel):
    name = models.CharField('标签', max_length=100)
    is_active = models.BooleanField('是否有效', default=True)

    class Meta:
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Article(BaseModel):
    title = models.CharField('标题', max_length=70)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, related_name="article_cat", on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    body = MDTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='作者')
    views = models.PositiveIntegerField('阅读量', default=0)
    is_recommend = models.BooleanField('是否推荐', default=False)
    is_active = models.BooleanField('是否有效', default=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'excerpt': self.excerpt,
            'category': self.category,
            'tags': self.tags,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def channel_to_dict(self):
        return {
            'title': self.title,
            'excerpt': self.excerpt,
            'body': self.body
        }


class ChainSafe(BaseModel):
    title = models.CharField(max_length=70, verbose_name='名称')
    author = models.CharField(max_length=70, verbose_name='作者')
    img = models.ImageField(
        upload_to='article_img/%Y/%m/%d/',
        blank=True, null=True, verbose_name='图片'
    )
    body = UEditorField(
        width=800, height=500, toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000}, settings={}, command=None, blank=True,
        verbose_name='内容'
    )
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='简介')
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    is_active = models.BooleanField(default=True, verbose_name='是否是开启')

    class Meta:
        verbose_name = '链安表'
        verbose_name_plural = '链安表'

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'img': str(self.img),
            'excerpt': self.excerpt,
            'views': self.views,
            'is_active': self.is_active
        }

    def channel_to_dict(self):
        return {
            'title': self.title,
            'excerpt': self.excerpt,
            'body': self.body
        }

