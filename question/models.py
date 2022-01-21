#encoding=utf-8

from django.db import models
from common.models import BaseModel, Category
from ceye_auth.models import User
from mdeditor.fields import MDTextField


BANNER_TYPE_CHOICES = [(x, x) for x in ['Index', 'Activity', 'Other']]
ANSWER_STATUS = [(x, x) for x in ['UnAnswer', 'Answered', 'Unknown']]


class Questions(BaseModel):
    title = models.CharField(max_length=70, verbose_name='标题')
    category = models.ForeignKey(
        Category, related_name="questions_cat",
        on_delete=models.DO_NOTHING, blank=True, null=True,
        verbose_name='问题分类',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='提问人')
    content = MDTextField()
    answers = models.PositiveIntegerField(default=0, verbose_name='答案个数')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    status = models.CharField(max_length=100, choices=ANSWER_STATUS, default="UnAnswer", db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')

    class Meta:
        verbose_name = '问题表'
        verbose_name_plural = '问题表'

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'answers': self.answers,
            'views': self.views,
            'status': self.status,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Answers(BaseModel):
    question = models.ForeignKey(
        Questions, related_name="questions_answers", on_delete=models.DO_NOTHING,
        blank=True, null=True,  verbose_name='问题'
    )
    user = models.ForeignKey(
        User, related_name="user_answers", on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='回答者'
    )
    content = MDTextField()
    is_active = models.BooleanField('是否是有效', default=True)

    class Meta:
        verbose_name = '回答表'
        verbose_name_plural = '回答表'

    def __str__(self):
        return self.content

    def as_dict(self):
        return {
            'id': self.id,
            'question': self.question.as_dict() if self.question is not None else None,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
