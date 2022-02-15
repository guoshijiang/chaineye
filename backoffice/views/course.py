# encoding=utf-8

import pytz
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from planet.models import (
    Course,
    CourseCat,
    CourseArtcle,
    CourseCommet,
)
from ceye_auth.models import User, UserInfo
from backoffice.helper import check_admin_login


@check_admin_login
def back_course_list(request):
    user_name = request.GET.get("user_name", "")
    title = request.GET.get("title", "")
    cat_id = int(request.GET.get("cat_id", 0))
    course_cat_list = CourseCat.objects.all().order_by("-id")
    course_list = Course.objects.all().order_by("-id")
    if user_name not in ["", "None"]:
        user = User.objects.filter(user_name=user_name).first()
        course_list = course_list.filter(user=user)
    if title not in ["", None]:
        course_list = course_list.filter(title=title)
    if cat_id not in [0, "0"]:
        cat = CourseCat.objects.filter(id=cat_id).first()
        course_list = course_list.filter(category=cat)
    total_course = len(course_list)
    course_list = paged_items(request, course_list)
    return render(request, 'admin/course/course_list.html', locals())


@check_admin_login
def back_course_check(request, cid):
    b_course = Course.objects.filter(id=cid).first()
    b_course.status = "CheckPass"
    b_course.is_active = True
    b_course.save()
    return redirect('back_course_list')


@check_admin_login
def back_course_artcle(request, cid):
    title = request.GET.get("title", "")
    course_article_list = CourseArtcle.objects.filter(course__id=cid).order_by("-id")
    if title not in ["", None]:
        course_article_list = course_article_list.filter(title=title)
    total_course_article = len(course_article_list)
    course_article_list = paged_items(request, course_article_list)
    return render(request, 'admin/course/course_artcle.html', locals())


@check_admin_login
def back_course_comment(request, aid):
    course_comment_list = CourseCommet.objects.filter(artcle__id=aid).order_by("-id")
    total_course_comment = len(course_comment_list)
    course_comment_list = paged_items(request, course_comment_list)
    return render(request, 'admin/course/artcle_comment.html', locals())