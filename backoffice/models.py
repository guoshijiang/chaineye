#encoding=utf-8

from django.db import models
from common.models import BaseModel, Category
from ceye_auth.models import User
from DjangoUeditor.models import UEditorField


class Message(BaseModel):
    title = models.CharField(max_length=70, verbose_name='标题')
    img = models.ImageField(
        upload_to='message_img/%Y/%m/%d/',
        verbose_name='图片',
        blank=True, null=True
    )
    content = UEditorField(
        width=800, height=500,
        toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}, command=None, blank=True, verbose_name='内容'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')

    class Meta:
        verbose_name = '公告表'
        verbose_name_plural = '公告表'

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'img': str(self.img),
            'content': self.content,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

