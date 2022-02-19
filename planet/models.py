#encoding=utf-8

from django.db import models
from common.models import BaseModel, DecField
from ceye_auth.models import User
from mdeditor.fields import MDTextField
from common.helpers import d0

CourseStatus = [
    (x, x) for x in ["Checking", "CheckFail", "CheckPass"]
]
YesOrNo = [
    (x, x) for x in ["Yes", "No"]
]


class CourseCat(BaseModel):
    name = models.CharField(max_length=100, verbose_name='名称')
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def return_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Course(BaseModel):
    title = models.CharField(max_length=100, verbose_name='课程标题')
    logo = models.ImageField(
        upload_to='block_logo/%Y/%m/%d/', blank=True,
        default="block_logo/2021/05/06/1.jpeg", null=True,
        verbose_name='课程图片'
    )
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='课程摘要')
    category = models.ForeignKey(
        CourseCat, related_name="course_cat", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='课程分类'
    )
    detail = MDTextField(
        null=True, blank=True, verbose_name='课程介绍'
    )
    price = DecField(
        default=d0, verbose_name="课程价格"
    )
    status = models.CharField(
        max_length=100,
        choices=CourseStatus,
        default="Checking",
        verbose_name="课程状态",
    )
    is_pre_sell = models.CharField(
        max_length=100,
        choices=YesOrNo,
        default="Yes",
        verbose_name="是否预售",
    )
    buyer_num = models.PositiveIntegerField(default=0, verbose_name='购买人数')
    article_num = models.PositiveIntegerField(default=0, verbose_name='课时数量')
    views = models.PositiveIntegerField(default=0, verbose_name='课程阅读量')
    process = models.CharField(max_length=100, default="0", verbose_name='课程完成度')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='作者')
    is_synced = models.BooleanField(default=False, verbose_name='是否已经同步')
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def channel_to_dict(self):
        return {
            'title': self.title,
            'logo': self.logo,
            'excerpt': self.excerpt,
            'detail': self.detail,
            'price': self.price,
            'buyer_num': self.buyer_num,
            'article_num': self.article_num,
            'views': self.views,
            'process': self.process
        }


class CourseArtcle(BaseModel):
    part = models.CharField(max_length=100, default="1", verbose_name='章节')
    title = models.CharField(max_length=100, verbose_name='文章标题')
    course = models.ForeignKey(
        Course, related_name="course_cs_arctcle", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='所属课程'
    )
    detail = MDTextField(
        null=True, blank=True, verbose_name='文章详细'
    )
    is_free = models.CharField(
        max_length=100,
        choices=YesOrNo,
        default="No",
        verbose_name="课程状态",
    )
    comment_num = models.PositiveIntegerField(default=0, verbose_name='文章阅读量')
    views = models.PositiveIntegerField(default=0, verbose_name='文章阅读量')
    is_synced = models.BooleanField(default=False, verbose_name='是否已经同步')
    is_active = models.BooleanField(default=False, verbose_name='是否是有效')

    class Meta:
        verbose_name = '课程文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'detail': self.detail,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def channel_to_dict(self):
        return {
            'part': self.part,
            'title': self.title,
            'detail': self.detail
        }


class CourseCommet(BaseModel):
    course = models.ForeignKey(
        Course, related_name="course_comment", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='评论的课程'
    )
    user = models.ForeignKey(
        User, related_name="course_user_comment", on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='回答者'
    )
    artcle = models.ForeignKey(
        CourseArtcle, related_name="comment_course_artcle", on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='评论的文章'
    )
    content = MDTextField()
    is_active = models.BooleanField('是否是有效', default=True)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = '课程评论'

    def __str__(self):
        return self.content

    def as_dict(self):
        return {
            'id': self.content,
        }