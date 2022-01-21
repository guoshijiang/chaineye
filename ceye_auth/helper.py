#encoding=utf-8

import logging
import random
import hashlib
import json
import requests
import time, datetime
import uuid
from django.http import HttpRequest
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache
from common.helpers import error_json, ok_json


TOEKN_INFO_EMPTY = 100
API_TOKEN_NOT_EXIST = 101
AUTH_TOKEN_NOT_EXIST = 102
API_TOKEN_EXPIRE = 103
API_TOKEN_STATUS = 104
AUTH_TOKEN_EXPIRE = 105
TOKEN_AUTH_OK = 200


# 阿里发送短信验证码
def send_msg_by_ali(phone_numbers: str, code: str):
    client = AcsClient(settings.ACCESSKEYID,
                       settings.ACCESSSECRET,
                       'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('http')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone_numbers)
    request.add_query_param('SignName', settings.SIGNNAME)
    request.add_query_param('TemplateCode', settings.TEMPLATECODE)
    request.add_query_param('TemplateParam', {"code": code})
    response = client.do_action(request)
    result = (str(response, encoding='utf-8'))
    return result


def get_code(number=6, alpha=False):
    verify_code = ''
    for i in range(number):
        num = random.randint(0, 9)
        if alpha is True:
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        verify_code = verify_code + str(num)
    return verify_code


def hash_code(data):
    s = str(data)
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()


def create_token():
    return uuid.uuid4()


def current_local_datetime():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def current_utc_ymd():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def edd_time_handle(days=0):
    date_time = current_utc_ymd()
    date_start = datetime.datetime.strptime(date_time, '%Y-%m-%d')
    date_start += datetime.timedelta(days=days)
    return str(date_start)


