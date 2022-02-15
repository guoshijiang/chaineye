# encoding=utf-8

import pytz
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from blogs.models import Article, Category, ChainSafe
from ceye_auth.models import User, UserInfo
from backoffice.helper import check_admin_login
from question.models import Questions
from activity.models import Activity


@check_admin_login
def back_index(request):
    user_name = request.GET.get("user_name", "")
    title = request.GET.get("title", "")
    cat_id = int(request.GET.get("cat_id", 0))
    blog_cat_list = Category.objects.all().order_by("-id")
    article_list = Article.objects.all().order_by("-id")
    if user_name not in ["", "None"]:
        user = User.objects.filter(user_name=user_name).first()
        article_list = article_list.filter(user=user)
    if title not in ["", None]:
        article_list = article_list.filter(title=title)
    if cat_id not in [0, "0"]:
        cat = Category.objects.filter(id=cat_id).first()
        article_list = article_list.filter(category=cat)
    total_article = len(article_list)
    article_list = paged_items(request, article_list)
    return render(request, 'admin/index/index.html', locals())


@check_admin_login
def back_blog_check(request, bid):
    b_blog = Article.objects.filter(id=bid).first()
    b_blog.is_active = True
    b_blog.save()
    return redirect('back_index')


@check_admin_login
def back_chainsafe(request):
    title = request.GET.get("title", "")
    chain_safe_list = ChainSafe.objects.all().order_by("-id")
    if title not in ["", None]:
        chain_safe_list = chain_safe_list.filter(title=title)
    total_chain_safe = len(chain_safe_list)
    chain_safe_list = paged_items(request, chain_safe_list)
    return render(request, 'admin/index/chain_safe.html', locals())


@check_admin_login
def back_chainsafe_check(request, id):
    chain_safe = ChainSafe.objects.filter(id=id).first()
    chain_safe.is_active = True
    chain_safe.save()
    return redirect('back_chainsafe')


@check_admin_login
def back_question_list(request):
    user_name = request.GET.get("user_name", "")
    title = request.GET.get("title", "")
    question_list = Questions.objects.all().order_by("-id")
    if user_name not in ["", "None"]:
        user = User.objects.filter(user_name=user_name).first()
        question_list = question_list.filter(user=user)
    if title not in ["", None]:
        question_list = question_list.filter(title=title)
    total_question = len(question_list)
    question_list = paged_items(request, question_list)
    return render(request, 'admin/index/question_list.html', locals())


@check_admin_login
def back_question_check(request, id):
    qs = Questions.objects.filter(id=id).first()
    qs.is_active = True
    qs.save()
    return redirect('back_question_list')


@check_admin_login
def back_activity_list(request):
    user_name = request.GET.get("user_name", "")
    title = request.GET.get("title", "")
    activity_list = Activity.objects.all().order_by("-id")
    if user_name not in ["", "None"]:
        user = User.objects.filter(user_name=user_name).first()
        activity_list = activity_list.filter(user=user)
    if title not in ["", None]:
        activity_list = activity_list.filter(title=title)
    total_activity = len(activity_list)
    activity_list = paged_items(request, activity_list)
    return render(request, 'admin/index/activity_list.html', locals())


@check_admin_login
def back_activity_check(request, id):
    act = Activity.objects.filter(id=id).first()
    act.is_active = True
    act.save()
    return redirect('back_activity_list')