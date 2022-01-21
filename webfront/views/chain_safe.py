#encoding=utf-8

import logging
from django.shortcuts import render, redirect
from blogs.models import ChainSafe
from common.helpers import paged_items


def chain_safe(request):
    nav_mark = "chain_safe"
    chain_safe_list = ChainSafe.objects.all().order_by("-id")
    chain_safe_list = paged_items(request, chain_safe_list, 30)
    return render(request, 'web/colleage/chain_safe.html', locals())


def chain_safe_detail(request, cid):
    nav_mark = "chain_safe"
    chain_safe = ChainSafe.objects.filter(id=cid).order_by("-id").first()
    chain_safe.views += 1
    chain_safe.save()
    return render(request, 'web/colleage/chain_safe_detail.html', locals())





