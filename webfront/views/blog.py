#encoding=utf-8

import pytz
import markdown
from django.shortcuts import render
from blogs.models import Category, Article, Tag
from common.helpers import ok_json, error_json
from django.conf import settings
from common.models import Category, Advertise, Banner, Partner
from webfront.hleper import judge_pc_or_mobile
from planet.models import Course

tz = pytz.timezone(settings.TIME_ZONE)


def global_variable(request):
    adv_list = Advertise.objects.filter(is_active=True).all()
    hot_tag = Tag.objects.filter(is_active=True).order_by("-id")[:60]
    article_list = Article.objects.filter(is_active=True).order_by('id')[:10]
    recd_art_list = Article.objects.filter(is_recommend=True).order_by('-views')[:10]
    partner_list = Partner.objects.filter(is_active=True).all()
    return locals()


def index(request):
    cat_id = int(request.GET.get('cat_id', 0))
    title = request.GET.get("title", "")
    user_agt = judge_pc_or_mobile(request.META.get("HTTP_USER_AGENT"))
    if title in ["", None]:
        banner_list = Banner.objects.filter(is_active=True)[0:4]
        hot_list = Article.objects.filter(is_active=True).order_by('views')[:3]
    cat_list = Category.objects.filter(type='Article', is_active=True).order_by("id").all()
    if cat_id not in ["0", 0, None]:
        cat = Category.objects.get(id=cat_id)
        index_article_lst = Article.objects.filter(
            category=cat,
            is_active=True
        ).order_by('-id')[:20]
    else:
        index_article_lst = Article.objects.filter(is_active=True).order_by('-id')[:20]
    if title not in ["", None]:
        index_article_lst = Article.objects.filter(title__icontains=title).order_by("-id")
    nav_mark = "index"
    if user_agt is False:
        return render(request, 'web/finance/index.html', locals())
    else:
        course_list = Course.objects.filter(status="CheckPass").order_by("views")[0:8]
        hot_blog_list = Article.objects.filter(is_active=True).order_by('views')[:20]
        return render(request, 'h5/index.html', locals())


def blog_list(request):
    cat_id = int(request.GET.get('cat_id', 0))
    title = request.GET.get("title", "")
    if title in ["", None]:
        hot_list = Article.objects.filter(is_active=True).order_by('-views')[:3]
        index = 1
        for hot in hot_list:
            hot.index = index
            index = index + 1
    cat_list = Category.objects.filter(type='Article', is_active=True).order_by("id").all()
    if cat_id not in ["0", 0, None]:
        cat = Category.objects.get(id=cat_id)
        index_article_lst = Article.objects.filter(
            category=cat,
            is_active=True
        ).order_by('-id')[:20]
    else:
        index_article_lst = Article.objects.filter(is_active=True).order_by('-id')[:20]
    if title not in ["", None]:
        index_article_lst = Article.objects.filter(title__icontains=title).order_by("-id")
    nav_mark = "index"
    return render(request, 'h5/blog/list.html', locals())



def article_list(request):
    cat_id = request.GET.get('cat_id', 0)
    page = int(request.GET.get('page', 20))
    cat_name = request.GET.get('cat_name', "")
    page_size = int(request.GET.get('page_size', 1))
    start = page * page_size
    end = start + page_size
    if cat_id in ["0", 0]:
        article_lst = Article.objects.filter(
            is_active=True
        ).order_by('-id')[start:end]
    else:
        cat = Category.objects.filter(id=cat_id).order_by("-id").first()
        article_lst = Article.objects.filter(
            category=cat,
            is_active=True
        ).order_by('-id')[start:end]
    article_list = []
    total = len(article_lst)
    for article in article_lst:
        created_at = article.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
        a_t_l = {
            "id": article.id,
            "title": article.title,
            "excerpt": article.excerpt,
            "img": str(article.img),
            'user': article.user.user_name,
            'views': article.views,
            'created_at': created_at,
        }
        article_list.append(a_t_l)
    ret_data = {
        "total": total,
        "data": article_list
    }
    return ok_json(ret_data)


def tag_list(request, tag):
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    tag_artcle_list = Article.objects.filter(tags__name=tag, is_active=True).order_by('-id')[start:end]
    tag_name = tag
    if request.is_ajax():
        article_list = []
        total = len(tag_artcle_list)
        for tag_artcle in tag_artcle_list:
            created_at = tag_artcle.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
            a_t_l = {
                "id": tag_artcle.id,
                "title": tag_artcle.title,
                "excerpt": tag_artcle.excerpt,
                "img": str(tag_artcle.img),
                'user': tag_artcle.user.get_username(),
                'views': tag_artcle.views,
                'created_at': created_at,
            }
            article_list.append(a_t_l)
        ret_data = {
            "total": total,
            "data": article_list
        }
        return ok_json(ret_data)
    else:
        return render(request, 'web/finance/tag_list.html', locals())


def arctle_detail(request):
    article_id = int(request.GET.get('article_id', 0))
    user_agt = judge_pc_or_mobile(request.META.get("HTTP_USER_AGENT"))
    article = Article.objects.filter(id=article_id).first()
    article.views += 1
    article.save()
    article.body = markdown.markdown(
        article.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    if user_agt is False:
        return render(request, 'web/finance/detail.html', locals())
    else:
        return render(request, 'h5/blog/detail.html', locals())


