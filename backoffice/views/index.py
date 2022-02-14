# encoding=utf-8

import pytz
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from blogs.models import Article, Category, ChainSafe
from ceye_auth.models import User, UserInfo


def back_index(request):
    user_id = int(request.GET.get("user_id", 0))
    title = request.GET.get("title", "")
    cat_id = int(request.GET.get("cat_id", 0))
    article_list = Article.objects.all().order_by("-id")
    if user_id not in [0, "0"]:
        user = User.objects.filter(id=user_id).first()
        article_list = article_list.filter(user=user)
    if title not in ["", None]:
        article_list = article_list.filter(title=title)
    if cat_id not in [0, "0"]:
        cat = Category.objects.filter(id=cat_id).first()
        article_list = article_list.filter(category=cat)
    article_list = paged_items(request, article_list)
    return render(request, 'admin/index/index.html', locals())


def back_chainsafe(request):
    title = request.GET.get("title", "")
    chain_safe_list = ChainSafe.objects.all().order_by("-id")
    if title not in ["", None]:
        chain_safe_list = chain_safe_list.filter(title=title)
    chain_safe_list = paged_items(request, chain_safe_list)
    return render(request, 'admin/index/chain_safe.html', locals())