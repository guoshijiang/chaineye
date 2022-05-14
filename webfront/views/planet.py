#encoding=utf-8

import pytz
import markdown
from django.shortcuts import render, redirect
from planet.forms.course_form import CourseForm
from planet.forms.course_arctle_form import CourseArtcleForm
from planet.forms.course_cmt_form import CourseCmtForm
from django.views.decorators.csrf import csrf_exempt
from planet.models import (
    Course,
    CourseCommet,
    CourseArtcle,
    CourseCat
)
from common.helpers import paged_items
from ceye_auth.models import User, UserInfo, UserBuyCourse
from wallet.models import UserWallet, TansRecord
from django.http import HttpResponseRedirect
from common.models import Asset


def plannet_course(request):
    nav_mark = "plannet_course"
    cat_id = request.GET.get("cat_id", 0)
    course_cat_list = CourseCat.objects.filter(is_active=True)
    course_list = Course.objects.filter(is_active=True, status="CheckPass").order_by("-id")
    if cat_id not in [0, "0"]:
        course_list = course_list.filter(category__id=cat_id)
    course_list = paged_items(request, course_list)
    return render(request, 'web/planet/course.html', locals())


@csrf_exempt
def course_detail(request, cid):
    nav_mark = "plannet_course"
    uid = request.session.get("user_id")
    user = User.objects.filter(id=uid).order_by("-id").first()
    user_wallet = UserWallet.objects.filter(user=user).order_by("-id").first()
    course_detail = Course.objects.filter(id=cid).first()
    course_arcticle_list = CourseArtcle.objects.filter(
        course=course_detail
    )
    course_detail.views = course_detail.views + 1
    course_detail.save()
    course_arcticle_first = course_arcticle_list.first()
    if request.method == "GET":
        ub_course = UserBuyCourse.objects.filter(user=user, course_id=cid).first()
        if ub_course is not None:
            already_buy = True
        return render(request, 'web/planet/course_detail.html', locals())
    if request.method == "POST":
        if user_wallet is None:
            wallet_not_exist = True
            return render(request, 'web/planet/course_detail.html', locals())
        ub_course = UserBuyCourse.objects.filter(user=user, course_id=cid).first()
        if ub_course is not None:
            already_buy = True
            return render(request, 'web/planet/course_detail.html', locals())
        else:
            course = Course.objects.filter(id=cid).first()
            if user_wallet.balance < course.price:
                balance_not_enough = True
                return render(request, 'web/planet/course_detail.html', locals())
            else:
                user_wallet.balance = user_wallet.balance - course.price
                user_wallet.save()
                UserBuyCourse.objects.create(
                    user=user,
                    course_id=cid
                )
                TansRecord.objects.create(
                    user=user,
                    asset=Asset.objects.filter(name="USDT").first(),
                    amount=course.price,
                    trans_way="Output",
                    source="购买课程消耗"
                )
                buy_success = True
                course_detail.buyer_num += 1
                course_detail.save()
                return render(request, 'web/planet/course_detail.html', locals())


def course_article_detail(request, arcticle_id):
    nav_mark = "plannet_course"
    uid = request.session.get("user_id")
    course_arcticle = CourseArtcle.objects.filter(id=arcticle_id).first()
    course_arcticle_list = CourseArtcle.objects.filter(
        course=course_arcticle.course
    )
    course_id = int(course_arcticle.course.id)
    course_detail = Course.objects.filter(id=course_id).first()
    course_detail.views = course_detail.views + 1
    course_detail.save()
    arcticle_comments = CourseCommet.objects.filter(artcle__id=arcticle_id).order_by("-id")
    course_arcticle.views += 1
    course_arcticle.save()
    course_arcticle.detail = markdown.markdown(
        course_arcticle.detail,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    if uid is None:
        not_buy_this_course = True
    ub_course = UserBuyCourse.objects.filter(user__id=uid, course_id=course_id).first()
    if ub_course is None:
        not_buy_this_course = True
    else:
        not_buy_this_course = False
    if request.method == "GET":
        comment_form = CourseCmtForm(request)
        return render(request, 'web/planet/course_article.html', locals())
    if request.method == "POST":
        comment_form = CourseCmtForm(request, request.POST)
        if comment_form.is_valid():
            n_course_arcticle = CourseArtcle.objects.filter(id=arcticle_id).first()
            n_course_arcticle.comment_num += 1
            n_course_arcticle.save()
            comment_form.db_create_course_cmt(course_arcticle.course, uid, course_arcticle)
            return redirect('course_article_detail', int(arcticle_id))
        else:
            error = comment_form.errors
            return render(
                request, "web/planet/course_article.html",
                {
                    "arcticle_comments": arcticle_comments,
                    "course_arcticle": course_arcticle,
                    "course_arcticle_list": course_arcticle_list,
                    'arcticle_id': int(arcticle_id),
                    'comment_form': comment_form,
                    'error': error
                }
            )


@csrf_exempt
def create_course(request, uid):
    nav_mark = "plannet_course"
    active_mark = "my_course"
    if request.method == "GET":
        user_id = uid
        course_form = CourseForm(request)
        return render(request, "web/auth/course/create_course.html", locals())
    if request.method == "POST":
        course_form = CourseForm(request, request.POST, request.FILES)
        if course_form.is_valid():
            course_form.db_create_course(int(uid))
            return redirect('my_course', int(uid))
        else:
            error = course_form.errors
            return render(
                request, "web/auth/course/create_course.html",
                {
                    'user_id': int(uid),
                    'course_form': course_form,
                    'error': error
                }
            )

@csrf_exempt
def update_course(request, cid):
    nav_mark = "plannet_course"
    active_mark = "my_course"
    course = Course.objects.filter(id=cid).first()
    uid = request.session.get("user_id")
    if request.method == "GET":
        course_form = CourseForm(request, instance=course)
        return render(request, "web/auth/course/update_course.html", locals())
    if request.method == "POST":
        course_form = CourseForm(request, request.POST, request.FILES, instance=course)
        if course_form.is_valid():
            uid = course_form.update_course(cid)
            return redirect('my_course', uid)
        else:
            error = course_form.errors
            return render(
                request, "web/auth/course/update_course.html",
                {
                    "user_id": uid,
                    "course": course,
                    'course_form': course_form,
                    'error': error
                }
            )


@csrf_exempt
def create_course_article(request, cid):
    nav_mark = "plannet_course"
    active_mark = "my_course"
    course_id = int(cid)
    c_article_list = CourseArtcle.objects.filter(course__id=cid)
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()
    user_info = UserInfo.objects.filter(user_id=user_id).first()
    if request.method == "GET":
        course_article_form = CourseArtcleForm(request)
        return render(request, "web/auth/course/add_course_time.html", locals())
    if request.method == "POST":
        course_article_form = CourseArtcleForm(request, request.POST)
        if course_article_form.is_valid():
            course_article_form.db_create_course(int(cid))
            return redirect('create_course_article', int(cid))
        else:
            error = course_article_form.errors
            return render(
                request, "web/auth/course/add_course_time.html",
                {
                    "c_article_list": c_article_list,
                    "user": user,
                    "user_info": user_info,
                    "course_id": course_id,
                    'user_id': int(user_id),
                    'course_article_form': course_article_form,
                    'error': error
                }
            )


@csrf_exempt
def wirte_course_article(request, act_id):
    nav_mark = "plannet_course"
    active_mark = "my_course"
    c_article = CourseArtcle.objects.filter(id=act_id).first()
    c_article_id = act_id
    uid = request.session.get("user_id")
    if request.method == "GET":
        course_article_form = CourseArtcleForm(request, instance=c_article)
        return render(request, "web/auth/course/wirte_course_arctle.html", locals())
    if request.method == "POST":
        course_article_form = CourseArtcleForm(request, request.POST, instance=c_article)
        if course_article_form.is_valid():
            uid = course_article_form.update_course(act_id)
            return redirect('create_course_article', int(c_article.course.id))
        else:
            error = course_article_form.errors
            return render(
                request, "web/auth/course/wirte_course_arctle.html",
                {
                    "user_id": uid,
                    "c_article": c_article,
                    'course_article_form': course_article_form,
                    'error': error
                }
            )

