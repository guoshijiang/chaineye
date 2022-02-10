#encoding=utf-8

import pytz
import markdown
from django.shortcuts import render
from blogs.models import Category, Article, Tag
from common.helpers import ok_json, error_json
from django.conf import settings
from common.models import Category, Advertise, Banner, Partner

tz = pytz.timezone(settings.TIME_ZONE)


def back_index(request):
    return locals()
