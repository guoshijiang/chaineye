#encoding=utf-8

import logging
from django.shortcuts import render, redirect
from blogs.models import ChainSafe
from common.helpers import paged_items
from webfront.hleper import judge_pc_or_mobile


def chain_safe(request):
    nav_mark = "chain_safe"
    user_agt = judge_pc_or_mobile(request.META.get("HTTP_USER_AGENT"))
    chain_safe_list = ChainSafe.objects.all().order_by("-id")
    chain_safe_list = paged_items(request, chain_safe_list, 30)
    if user_agt is False:
        return render(request, 'web/colleage/chain_safe.html', locals())
    else:
        return render(request, 'h5/chain_safe/list.html', locals())


def chain_safe_detail(request, cid):
    nav_mark = "chain_safe"
    user_agt = judge_pc_or_mobile(request.META.get("HTTP_USER_AGENT"))
    chain_safe = ChainSafe.objects.filter(id=cid).order_by("-id").first()
    chain_safe.views += 1
    chain_safe.save()
    if user_agt is False:
        return render(request, 'web/colleage/chain_safe_detail.html', locals())
    else:
        return render(request, 'h5/chain_safe/detail.html', locals())






