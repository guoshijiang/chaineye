#encoding=utf-8

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


@check_bearer_auth
def get_chainsafe():
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    cf_data_list = []
    cf_list = ChainSafe.objects.filter(is_active=True).order_by("-id")[start:end]
    for cf in cf_list:
        cf_data_list.append(cf.channel_to_dict())
    return ok_json(cf_data_list)

@check_bearer_auth
def get_blogs():
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    article_data_list = []
    article_list = Article.objects.filter(is_active=True).order_by("-id")[start:end]
    for article in article_list:
        article_data_list.append(article.channel_to_dict())
    return ok_json(article_data_list)

@check_bearer_auth
def get_course():
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    course_data_list = []
    course_list = Course.objects.filter(is_active=True).order_by("-id")[start:end]
    for course in course_list:
        course_article_data_list = []
        ca_list = CourseArtcle.ojects.filter(course=course).order_by("-id")
        for ca in ca_list:
            course_article_data_list.apend(ca.channel_to_dict())
        return_data = {
            "article": article.channel_to_dict(),
            "course_article": course_article_data_list
        }
        course_data_list.append(return_data)
    return ok_json(course_data_list)
