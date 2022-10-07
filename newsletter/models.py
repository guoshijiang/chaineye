#encoding=utf-8

from django.db import models
from ceye_auth.models import User
from common.models import BaseModel, Category
from DjangoUeditor.models import UEditorField


class Newsletter(BaseModel):
    title = models.CharField('标题', max_length=70)
    img = models.ImageField(upload_to='newsletter/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    content = UEditorField(
        width=800, height=500, toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000}, settings={}, command=None, blank=True,
        verbose_name='内容'
    )
    views = models.PositiveIntegerField('阅读量', default=0)
    is_letter = models.BooleanField(default=True, verbose_name='是不是快讯')
    category = models.ForeignKey(
        Category,
        related_name="newsletter_cat",
        on_delete=models.DO_NOTHING,
        verbose_name='分类',
        blank=True,
        null=True
    )
    good = models.PositiveIntegerField('利好', default=0)
    bad = models.PositiveIntegerField('利空', default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='作者'
    )

    class Meta:
        verbose_name = '快讯'
        verbose_name_plural = '快讯'

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'img': str(self.img),
            'excerpt': self.excerpt,
            'content': self.content,
            'category': self.category.name,
            'good': self.good,
            'bad': self.bad,
            'views': self.views,
            'user': self.user.user_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
