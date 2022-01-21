#encoding=utf-8

import pytz
from django.shortcuts import render, reverse, redirect
from blogs.models import Category
from activity.models import Activity, Area, PartActivity, SponsorActivity, CoinAddress
from common.helpers import ok_json, error_json
from django.conf import settings
from django.db.models import F, Q
from ceye_auth.models import User
from webfront.forms.activity_forms import ActivityForm
from django.views.decorators.csrf import csrf_exempt


def activity(request):
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 20))
    cat_id = int(request.GET.get('cat_id', 0))
    area_id = int(request.GET.get('area_id', 0))
    nav_mark = "activity"
    activity_cat = Category.objects.filter(type="Activity").all()
    area_list = Area.objects.all()
    hot_act = Activity.objects.filter(is_active=True).order_by('views')[:8]
    start = page * page_size
    end = start + page_size
    if cat_id in ["0", 0] and area_id in ["0", 0]:
        activity_list = Activity.objects.all().order_by('-id')[start:end]
    else:
        category = Category.objects.filter(id=cat_id, type="'Activity").order_by("-id").first()
        area = Area.objects.filter(id=area_id).order_by("-id").first()
        activity_list = Activity.objects.filter(Q(category=category) | Q(area=area)).order_by('-id')[start:end]
    total = Activity.objects.all().count()
    ret_activity_list = []
    if request.is_ajax():
        for activity in activity_list:
            ret_activity_list.append(activity.as_list_dict())
        result = {
            "total": total,
            "data": ret_activity_list
        }
        return ok_json(result)
    else:
        return render(request, 'web/activity/activity.html', locals())


def activity_detail(request, id):
    nav_mark = "activity"
    activity_detail = Activity.objects.get(id=id)
    hot_activity = Activity.objects.all().order_by('?')[:10]
    previous_blog = Activity.objects.filter(
        created_at__gt=activity_detail.created_at,
        category=activity_detail.category.id
    ).first()
    netx_blog = Activity.objects.filter(
        created_at__lt=activity_detail.created_at,
        category=activity_detail.category.id
    ).last()
    activity_detail.views = activity_detail.views + 1
    activity_detail.save()
    sa_list = SponsorActivity.objects.filter(activity=activity_detail)
    return render(request, 'web/activity/activity_detail.html', locals())


def activity_tag(request, tag):
    nav_mark = "activity"
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 10))
    t_name = Area.objects.get(name=tag)
    start = page * page_size
    end = start + page_size
    activity_list = Activity.objects.filter(tags__name=tag)[start: end]
    total = Activity.objects.filter(tags__name=tag).count()
    ret_activity_list = []
    if request.is_ajax():
        for activity in activity_list:
            ret_activity_list.append(activity.as_list_dict())
        result = {
            "total": total,
            "data": ret_activity_list
        }
        return ok_json(result)
    else:
        return render(request, 'web/activity/activity_tag.html', locals())


@csrf_exempt
def participate_act(request, id):
    nav_mark = "activity"
    if request.method == 'GET':
        activity_id = id
        return render(request, 'web/activity/participate_act.html', locals())
    if request.method == 'POST':
        username = request.POST.get('username', "")
        account_id = request.POST.get('account_id', 0)
        activity_id = request.POST.get('activity_id', 0)
        phone = request.POST.get('phone', "")
        weichat = request.POST.get('weichat', "")
        email = request.POST.get('email', "")
        company = request.POST.get('company', "")
        position = request.POST.get('position', "")
        content = request.POST.get('content', "")
        act = Activity.objects.filter(id=activity_id).order_by("-id").first()
        title = "参加活动成功"
        redict_url = 'activity_detail'
        if act is None:
            error_msg = "参加活动失败,没有这个活动, 请重新选择活动加入"
            return render(request, 'web/temp.html', locals())
        user = User.objects.filter(id=account_id).order_by("-id").first()
        if user is None:
            title = "参加活动成功"
            error_msg = "参加活动失败，您还没有登陆, 请先去登陆再来选择参加的活动"
            return render(request, 'web/temp.html', locals())
        part_act = PartActivity.objects.create(
            user=user,
            activity=act,
            username=username,
            phone=phone,
            weichat=weichat,
            email=email,
            company=company,
            position=position,
            content=content,
        )
        error_msg = "参加活动成功, 请去我的里面查看详细信息"
        return render(request, 'web/temp.html', locals())


@csrf_exempt
def sponsor_act(request, id):
    nav_mark = "activity"
    if request.method == 'GET':
        activity_id = id
        coin_addr_list = CoinAddress.objects.all()
        return render(request, 'web/activity/sponsor_act.html', locals())
    if request.method == 'POST':
        name = request.POST.get('name', "")
        account_id = request.POST.get('account_id', 0)
        activity_id = request.POST.get('activity_id', 0)
        coin = request.POST.get('coin', "")
        amount = request.POST.get('amount', "")
        address = request.POST.get('address', "")
        phone = request.POST.get('phone', "")
        email = request.POST.get('email', "")
        company = request.POST.get('company', "")
        reason = request.POST.get('reason', "")
        act = Activity.objects.filter(id=activity_id).order_by("-id").first()
        title = "赞助活动成功"
        redict_url = 'activity_detail'
        if act is None:
            error_msg = "赞助活动失败,没有这个活动, 请重新选择活动赞助"
            return render(request, 'web/temp.html', locals())
        user = User.objects.filter(id=account_id).order_by("-id").first()
        if user is None:
            title = "赞助活动成功"
            error_msg = "赞助活动失败，您还没有登陆, 请先去登陆再来选择想要赞助的活动"
            return render(request, 'web/temp.html', locals())
        create_sa = SponsorActivity.objects.create(
            user=user,
            activity=act,
            name=name,
            coin=coin,
            amount=amount,
            address=address,
            phone=phone,
            email=email,
            company=company,
            reason=request,
        )
        error_msg = "赞助活动成功, 赞助信息将显示在活动的底部"
        return render(request, 'web/temp.html', locals())


@csrf_exempt
def publish_activity(request, uid):
    active_mark = "my_activity"
    if request.method == "GET":
        act_form = ActivityForm(request)
        return render(request, "web/auth/activity/create_activity.html", locals())
    if request.method == "POST":
        act_form = ActivityForm(request, request.POST, request.FILES)
        print("act_form ===", act_form)
        if act_form.is_valid():
            act_form.create_activity(uid)
            return redirect('my_activity', int(uid))
        else:
            error = act_form.errors
            return render(
                request, "web/auth/activity/create_activity.html",
                {
                    'user_id': int(uid),
                    'act_form': act_form,
                    'error': error
                }
            )


@csrf_exempt
def update_activity(request, act_id):
    active_mark = "my_activity"
    acty = Activity.objects.filter(id=act_id).first()
    if request.method == "GET":
        act_form = ActivityForm(request, instance=acty)
        return render(request, "web/auth/activity/update_activity.html", locals())
    if request.method == "POST":
        act_form = ActivityForm(request, request.POST, request.FILES, instance=acty)
        if act_form.is_valid():
            act_form.update_activity(acty.id)
            return redirect('my_activity', acty.user.id)
        else:
            error = act_form.errors
            return render(
                request, "web/auth/activity/update_activity.html",
                {
                    'act_form': act_form,
                    'error': error
                }
            )



