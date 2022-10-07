#encoding=utf-8

import logging
from django.core import serializers
from django.shortcuts import render, redirect
from django.db.models import F
from django.urls import reverse
from newsletter.models import Newsletter, Category
from common.helpers import paged_items, ok_json, error_json, parse_int
from webfront.hleper import judge_pc_or_mobile


def newsletter(request):
    nav_mark = "newsletter"
    cat_id = int(request.GET.get('cat_id', 0))
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    start = (page - 1) * page_size
    end = start + page_size
    user_agt = judge_pc_or_mobile(request.META.get("HTTP_USER_AGENT"))
    newsletter_cat_list = Category.objects.filter(type="NewsLetter").order_by("id")
    if cat_id not in ["0", 0, None]:
        allnewsletter = Newsletter.objects.filter(
            category__id=cat_id
        ).order_by('-id')
    else:
        allnewsletter = Newsletter.objects.all().order_by('-id')
    allnewsletter = paged_items(request, allnewsletter)
    if request.is_ajax():
        if cat_id == 0:
            allnewsletter = Newsletter.objects.all().order_by('-id')[start:end]
        else:
            allnewsletter = Newsletter.objects.filter(
                category__id=cat_id
            ).order_by('-id')[start:end]
        return_newsletter_data = []
        for newsletter in allnewsletter:
            return_newsletter_data.append(newsletter.as_dict())
        return ok_json(return_newsletter_data)
    if user_agt:
        return render(request, 'web/newsletter/newsletter.html', locals())
    else:
        return render(request, 'web/newsletter/newsletter.html', locals())



def newsgood(request):
    news_id = request.GET.get("id")
    Newsletter.objects.filter(id=news_id).update(good=F('good') + 1)
    newsletter_model = Newsletter.objects.filter(id=news_id).values('good')
    total_good = newsletter_model[0]['good']
    data = {
        "total_good": total_good
    }
    return ok_json(data)


def newsbad(request):
    news_id = request.GET.get("id")
    Newsletter.objects.filter(id=news_id).update(bad=F('bad') + 1)
    newsletter_model = Newsletter.objects.filter(id=news_id).values('bad')
    print(newsletter_model)
    total_bad = newsletter_model[0]['bad']
    data = {
        "total_bad": total_bad
    }
    return ok_json(data)



def newsletter_detail(request, id):
    nav_mark = "newsletter"
    user_agt = judge_pc_or_mobile(request.META.get("HTTP_USER_AGENT"))
    newsletter = Newsletter.objects.filter(id=id).first()
    newsletter.views += 1
    newsletter.save()
    if user_agt is False:
        return render(request, 'web/newsletter/newsletter_detail.html', locals())
    else:
        return render(request, 'web/newsletter/newsletter_detail.html', locals())
