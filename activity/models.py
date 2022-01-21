#encoding=utf-8

from django.db import models
from DjangoUeditor.models import UEditorField
from common.models import BaseModel, Category
from ceye_auth.models import User


ACTIVITY_STATUS = [(x, x) for x in ['UnStart', 'Starting', 'Finished']]
YES_OR_NO = [(x, x) for x in ['Yes', 'No']]


# 活动地区
class Area(BaseModel):
    name = models.CharField('活动地区', max_length=100)
    is_active = models.BooleanField('是否是有效', default=True)

    class Meta:
        verbose_name = '活动地区'
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


# 活动
class Activity(BaseModel):
    title = models.CharField(max_length=70, verbose_name='活动标题')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='活动分类'
    )
    position = models.TextField(max_length=200, blank=True, verbose_name='活动地点')
    area = models.ForeignKey(
        Area, on_delete=models.DO_NOTHING,
        null=True, blank=True,
        verbose_name='活动地区'
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='发布活动的用户'
    )
    act_time = models.TextField(max_length=200, blank=True, verbose_name='活动时间')
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='活动摘要')
    company = models.TextField(max_length=200, blank=True, verbose_name='主办单位')
    author = models.CharField(max_length=70, verbose_name='活动发起人')
    actfee = models.CharField(max_length=70, verbose_name='活动费用')
    person = models.CharField(max_length=70, verbose_name='人数上限')
    is_help = models.CharField(
        max_length=70,
        choices=YES_OR_NO,
        default="No",
        verbose_name='活动是否需要赞助'
    )
    img = models.ImageField(
        upload_to='article_img/%Y/%m/%d/',
        verbose_name='活动图片',
        blank=True,
        null=True
    )
    body = UEditorField(
        width=800, height=500,
        toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}, command=None, blank=True, verbose_name='内容'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    status = models.CharField(
        max_length=70, choices=ACTIVITY_STATUS,
        default="Starting", verbose_name='活动状态'
    )
    is_active = models.BooleanField(default=True, verbose_name='是否是开启活动')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'

    def __str__(self):
        return self.title

    def as_list_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'position': self.position,
            'excerpt': self.excerpt,
            'company': self.company,
            'act_time': self.act_time,
        }


# 参加活动
class PartActivity(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='参加活动的用户'
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='参加的活动'
    )
    username = models.CharField(max_length=100, default="", verbose_name='参加活动的姓名')
    phone = models.CharField(max_length=100, default="", verbose_name='参加活动人的联系电话')
    weichat = models.CharField(max_length=100, default="", verbose_name='联系微信')
    email = models.CharField(max_length=100, default="", verbose_name='联系邮箱')
    company = models.CharField(max_length=100, default="", verbose_name='公司')
    position = models.CharField(max_length=100, default="", verbose_name='职位')
    content = models.TextField(max_length=200, default="", verbose_name='参加活动的目的')

    class Meta:
        verbose_name = '活动参加表'
        verbose_name_plural = '活动参加表'

    def __str__(self):
        return self.username

    def as_list_dict(self):
        return {
            'id': self.id,
            'user': self.user.user_name,
            'activity': self.activity.title,
            'username': self.username,
            'phone': self.phone,
            'weichat': self.weichat,
            'email': self.email,
            'position': self.position,
            'content': self.content,
        }


# 赞助活动
class SponsorActivity(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True,
        null=True, verbose_name='赞助的用户'
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='赞助的活动'
    )
    name = models.CharField(max_length=100, default="", verbose_name='参加活动的姓名')
    coin = models.CharField(max_length=100, default="", verbose_name='赞助的币种')
    amount = models.CharField(max_length=100, default="0", verbose_name='赞助金额')
    address = models.CharField(max_length=100, default="", verbose_name='地址')
    phone = models.CharField(max_length=100, default="", verbose_name='赞助人手机号码')
    email = models.CharField(max_length=100, default="", verbose_name='赞助人邮箱')
    company = models.CharField(max_length=100, default="", verbose_name='赞助人公司')
    reason = models.TextField(max_length=200, default="", verbose_name='赞助原因')

    class Meta:
        verbose_name = '活动赞助表'
        verbose_name_plural = '活动赞助表'

    def __str__(self):
        return self.name

    def as_list_dict(self):
        return {
            'id': self.id,
            'user': self.user.user_name,
            'activity': self.activity.title,
            'name': self.name,
            'amount': self.amount,
            'phone': self.phone,
            'email': self.email,
            'company': self.company,
            'reason': self.reason
        }


# 币种地址表
class CoinAddress(BaseModel):
    coin = models.CharField(max_length=100, default="USDT", verbose_name='赞助的币种')
    address = models.CharField(max_length=100, default="", verbose_name='地址表')

    class Meta:
        verbose_name = '币种地址表'
        verbose_name_plural = '币种地址表'

    def __str__(self):
        return self.coin

    def as_dict(self):
        return {
            'id': self.id,
            'coin': self.coin,
            'address': self.address
        }