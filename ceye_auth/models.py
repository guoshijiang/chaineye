#encoding=utf-8

from django.db import models
from common.models import BaseModel, IdField, DecField


SEX_CHOICES = [(x, x) for x in ['男', '女', '未知']]
EXPIRED = 1
UNEXPIRE = 2
EXPIRE_TYPE_CHOICES = [(EXPIRED, 'EXPIRED'), (UNEXPIRE, 'UNEXPIRE')]
BackendAccountType = [(x, x) for x in ['Admin', "Outer", 'Inner']]
ValidSelect = [(x, x) for x in ['Yes', 'No']]


class Account(BaseModel):
    name = models.CharField(max_length=32, unique=True)
    role = models.CharField(
        max_length=128,
        choices=BackendAccountType,
        default="Admin",
        verbose_name=u'账户角色'
    )
    password = models.CharField(
        max_length=128,
        default='',
        verbose_name=u'密码'
    )
    valid = models.CharField(
        max_length=128,
        choices=ValidSelect,
        default="Yes",
        verbose_name=u'是否有效'
    )

    class Meta:
        verbose_name = '后台用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "role": self.role,
            "valid": self.valid,
        }


class User(BaseModel):
    user_name = models.CharField(max_length=32, default='', verbose_name=u'用户名')
    password = models.CharField(max_length=128, default='', verbose_name=u'密码')
    token = models.CharField(max_length=256, default='', verbose_name=u'token')
    token_is_expire = models.IntegerField(default=UNEXPIRE, choices=EXPIRE_TYPE_CHOICES)
    phone = models.CharField(max_length=16, default='', verbose_name=u'手机')
    loginip = models.CharField(max_length=128, default='', verbose_name=u'登陆IP')
    regtime = models.DateTimeField(auto_now=True, db_index=True, verbose_name=u'注册时间')
    logintime = models.DateTimeField(auto_now=True, db_index=True, verbose_name=u'登陆时间')

    class Meta:
        pass

    def __str__(self):
        return self.user_name

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "password": self.password,
            "token": self.token,
            "token_is_expire": self.token_is_expire,
            "phone": self.phone,
            "loginip": self.loginip,
            "regtime": self.regtime,
            "logintime": self.logintime,
        }


class UserInfo(BaseModel):
    real_name = models.CharField(max_length=64, default='', verbose_name=u'真实名字')
    photo = models.ImageField(upload_to='user_img/%Y/%m/%d/', blank=True, null=True, verbose_name=u'头像')
    introduce = models.TextField(max_length=512, blank=True, default='', verbose_name=u'简介')
    sex = models.CharField(max_length=16, choices=SEX_CHOICES, default='未知', verbose_name=u'性别')
    position = models.CharField(max_length=16, default='', verbose_name=u'职位')
    company = models.CharField(max_length=16, default='', verbose_name=u'单位')
    email = models.CharField(max_length=128, default='', verbose_name=u'邮件')
    user_id = IdField(default='', db_index=True, verbose_name=u'用户ID')
    qq = models.CharField(default='', max_length=128, verbose_name=u'QQ')
    wechat = models.CharField(default='', max_length=128, verbose_name='微信')

    class Meta:
        pass

    def __str__(self):
        return self.real_name

    def to_dict(self):
        return {
            "real_name": self.real_name,
            "photo": str(self.photo),
            "introduce": self.introduce,
            "sex": self.sex,
            "position": self.position,
            "company": self.company,
            "email": self.email,
            "user_id": self.user_id,
            'qq': self.qq,
            'wechat': self.wechat,
        }


class UserBuyCourse(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=u'购买人')
    course_id = IdField(default='', db_index=True, verbose_name=u'购买的课程ID')

    class Meta:
        verbose_name = '用户购买课程表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ""

    def as_dict(self):
        return {
            'id': self.id
        }