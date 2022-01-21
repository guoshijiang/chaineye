#encoding=utf-8

import time
import pytz
from django import template
from django.conf import settings
from ceye_auth.models import User, UserInfo
from decimal import Decimal
from common.helpers import d0


register = template.Library()


@register.filter(name='hdatetime')
def repr_datetime(value) -> str:
    if not value:
        return ''
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')


@register.filter(name='cn_hdatetime')
def cn_hdatetime(value) -> str:
    if not value:
        return ''
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime('%m月%d日 %H:%M')


@register.filter(name='act_status')
def act_status(value):
    return {
        'UnStart': '未开始',
        'Starting': '进行中',
        'Finished': '已结束',
    }.get(value, '')


@register.filter(name='account_info')
def account_info(value):
    if value in [0, '0', '', None]:
        return "游客"
    else:
        user = User.objects.filter(
            id=int(value)).order_by("-id").first()
        return user.user_name


@register.filter(name='check_status')
def check_status(value):
    return {
        'checked': '已审核',
        'uncheck': '未审核',
        'end': '已结束',
    }.get(value, '')


@register.filter(name='answer_status')
def answer_status(value):
    return {
        'UnAnswer': '未回答',
        'Answered': '已回答',
        'Unknown': '未知',
    }.get(value, '')


@register.filter(name="keep_two_decimal_places")
def ktd_places(value):
    if value in ["", None, "None", 0, d0]:
        return "0"
    dec_value = Decimal(value).quantize(Decimal("0.00"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )


@register.filter(name="user_photo")
def user_photo(value):
    u_info = UserInfo.objects.filter(user_id=value).first()
    return u_info.photo


@register.filter(name="user_position")
def user_position(value):
    u_info = UserInfo.objects.filter(user_id=value).first()
    return u_info.position