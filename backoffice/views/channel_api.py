#encoding=utf-8

import logging
import re
import uuid
import json
import pytz
from django.shortcuts import render, reverse, redirect
from common.helpers import ok_json, error_json
from django.conf import settings
from django.db.models import F, Q
from ceye_auth.models import User
from django.views.decorators.csrf import csrf_exempt
from blogs.models import Article, ChainSafe
from planet.models import Course, CourseArtcle
from backoffice.helper import check_bearer_auth
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@check_bearer_auth
def get_chainsafe(request):
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    cf_data_list = []
    cf_list = ChainSafe.objects.filter(is_active=True, is_synced=False).order_by("-id")[start:end]
    for cf in cf_list:
        cf_data_list.append(cf.channel_to_dict())
        cf.is_synced = True
        cf.save()
    return ok_json(cf_data_list)


@csrf_exempt
@check_bearer_auth
def get_blogs(request):
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    article_data_list = []
    article_list = Article.objects.filter(is_active=True, is_synced=False).order_by("-id")[start:end]
    for article in article_list:
        article_data_list.append(article.channel_to_dict())
        article.is_synced = True
        article.save()
    return ok_json(article_data_list)


@csrf_exempt
@check_bearer_auth
def get_course(request):
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    course_data_list = []
    course_list = Course.objects.filter(is_active=True, is_synced=False).order_by("-id")[start:end]
    for course in course_list:
        course_article_data_list = []
        course.is_synced = True
        course.save()
        ca_list = CourseArtcle.objects.filter(course=course).order_by("-id")
        for ca in ca_list:
            course_article_data_list.append(ca.channel_to_dict())
            ca.is_synced = True
            ca.save()
        return_data = {
            "article": course.channel_to_dict(),
            "course_article": course_article_data_list
        }
        course_data_list.append(return_data)
    return ok_json(course_data_list)
