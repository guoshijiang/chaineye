#encoding=utf-8

import logging
import markdown
import qrcode
import io
import base64
from ceye_auth.helper import send_msg_by_ali, get_code, hash_code
from django.core.cache import cache
from common.helpers import ok_json, error_json, paged_items
from ceye_auth.models import User, UserInfo
from django.shortcuts import render
from django.shortcuts import redirect
from blogs.models import Article
from activity.models import Activity, PartActivity, SponsorActivity
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from blogs.forms.arctle_forms import ArtcleForm
from question.models import Questions
from planet.models import Course
from common.models import Asset
from wallet.models import UserWallet
from webfront.wallet_adapter import create_address
from ceye_auth.models import UserBuyCourse



def sms_send(request):
    phone = request.GET.get('phone')
    code = get_code(6,  False)
    cache.set(phone, code, 60)
    if cache.has_key(phone):
        result = send_msg_by_ali(phone, code)
        return ok_json(result)


def sms_check(request):
    phone = request.GET.get('phone')
    code = request.GET.get('code')
    cache_code = cache.get(phone)
    if code == cache_code:
        return ok_json("ok")
    else:
        return error_json("False")


@csrf_exempt
def register(request):
    if request.session.get('is_login', None):
        return error_json("登录状态不允许注册！", 1000)
    phone = request.POST.get('phone')
    verify_code = request.POST.get('code')
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if verify_code != cache.get(phone):
        return error_json("验证码不正确！", 1000)
    if password1 != password2:
        return error_json("两次输入的密码不同！", 1000)
    else:
        try:
            same_name_user = User.objects.filter(phone=phone)
            if same_name_user:
                return error_json("用户已经存在，请重新选择用户名！", 1000)
        except:
            pass
        new_user = User.objects.create(
            phone=phone,
            user_name=username,
            password=hash_code(password1)
        )
        address_list = create_address(new_user.id)
        for addr in address_list:
            if addr.get("asset_name") == "USDT" and addr.get("chain_name") == "Tron":
                UserWallet.objects.create(
                    user=new_user,
                    asset=Asset.objects.filter(name="USDT").first(),
                    chain_name="Tron",
                    address=addr.get("address", None)
                )
        UserInfo.objects.create(
            user_id=new_user.id
        )
        return ok_json(new_user.to_dict())


@csrf_exempt
def login_by_verify_code(request):
    phone = request.POST.get("phone", "")
    verify_code = request.POST.get("code", "")
    if request.session.get('is_login', None):
        return error_json("该账号已经登陆！", 1000)
    if verify_code != cache.get(phone):
        return error_json("验证码不正确！", 1000)
    try:
        user = User.objects.get(phone=phone)
        try:
            userinfo = UserInfo.objects.get(user_id=user.id)
            request.session['user_pho'] = userinfo.user_pho
        except:
            request.session['user_pho'] = ''

        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['user_name'] = user.user_name
        return ok_json(user.to_dict())
    except:
        return error_json("用户不存在！", 1000)


@csrf_exempt
def login_by_verify_passwd(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    if request.session.get('is_login', None):
        return error_json("该账号已经登陆！", 1000)
    try:
        user = User.objects.filter(Q(user_name=username) | Q(phone=username)).order_by("-id").first()
        try:
            userinfo = UserInfo.objects.get(user_id=user.id)
            request.session['user_pho'] = str(userinfo.user_pho)
        except:
            request.session['user_pho'] = ''
        if user.password == hash_code(password):
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name
            return ok_json(user.to_dict())
        else:
            return error_json("密码不正确！", 1000)
    except:
        return error_json("用户不存在！", 1000)


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')


def my(request, uid):
    active_mark = "my"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    return render(request, 'web/auth/my.html', locals())


@csrf_exempt
def update_user_info(request, uid):
    user_id = request.POST.get("user_id")
    user_name = request.POST.get("user_name")
    user_company = request.POST.get("user_company", "")
    user_position = request.POST.get("user_position", "")
    user_photo = request.FILES.get('user_photo')
    user_sex = request.POST.get("user_sex", "")
    user_introduce = request.POST.get("user_introduce", "")
    user = User.objects.filter(id=user_id).order_by("-id").first()
    if user is not None:
        user.user_name = user_name
        user.save()
        user_info = UserInfo.objects.filter(user_id=user_id).order_by("-id").first()
        if user_info is not None:
            user_info.sex = user_sex
            user_info.introduce = user_introduce
            user_info.company = user_company
            user_info.position = user_position
            user_info.photo = user_photo
            user_info.save()
    return redirect('/' + str(user_id) + '/my')


def my_article(request, uid):
    active_mark = "my_article"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    article_list = Article.objects.filter(user__id=uid).order_by("-id")
    article_list = paged_items(request, article_list)
    return render(request, 'web/auth/artcle/my_actcle.html', locals())


@csrf_exempt
def create_article(request, uid):
    active_mark = "my_article"
    if request.method == "GET":
        user_id = uid
        art_form = ArtcleForm(request)
        return render(request, "web/auth/artcle/create_artcle.html", locals())
    if request.method == "POST":
        art_form = ArtcleForm(request, request.POST, request.FILES)
        if art_form.is_valid():
            art_form.db_create_arctcle(int(uid))
            return redirect('my_article', int(uid))
        else:
            error = art_form.errors
            return render(
                request, "web/auth/artcle/create_artcle.html",
                {
                    'user_id': int(uid),
                    'art_form': art_form,
                    'error': error
                }
            )


def update_article(request, arc_id):
    active_mark = "my_article"
    arctcle = Article.objects.filter(id=arc_id).first()
    uid = request.session.get("user_id")
    if request.method == "GET":
        art_form = ArtcleForm(request, instance=arctcle)
        return render(request, "web/auth/artcle/update_artcle.html", locals())
    if request.method == "POST":
        art_form = ArtcleForm(request, request.POST, request.FILES, instance=arctcle)
        if art_form.is_valid():
            uid = art_form.update_arctcle(arc_id)
            tip_msg = "修改密码成功, 请记住您的新密码"
            return redirect('my_article', uid)
        else:
            error = art_form.errors
            return render(
                request, "web/auth/artcle/update_artcle.html",
                {
                    "user_id": uid,
                    "arc_id": arc_id,
                    'art_form': art_form,
                    'error': error
                }
            )


def my_activity(request, uid):
    active_mark = "my_activity"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    act_list = Activity.objects.filter(user__id=uid)
    for act in act_list:
        act.join_num = PartActivity.objects.filter(activity=act).count()
    act_list = paged_items(request, act_list)
    return render(request, 'web/auth/activity/my_activity.html', locals())


def my_questions(request, uid):
    active_mark = "my_questions"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    qs_list = Questions.objects.filter(user__id=uid)
    qs_list = paged_items(request, qs_list)
    return render(request, 'web/questions/my_question.html', locals())


def my_wallet(request, uid):
    tab = "walletInfo"
    active_mark = "my_wallet"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    user_id = int(request.session.get("user_id"))
    asset_db = Asset.objects.get(name="USDT")
    user_wallet = UserWallet.objects.filter(user__id=user_id, asset=asset_db).first()
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(user_wallet.address)
    img = qr.make(fit=True)
    out = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out, 'PNG')
    data_steam = u"data:image/png;base64," + base64.b64encode(out.getvalue()).decode('ascii')
    return render(request, 'web/auth/wallet/my_wallet.html', locals())


def my_course(request, uid):
    active_mark = "my_course"
    course_name = request.GET.get("course_name", "")
    pay_way = request.GET.get("pay_way", "all")
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    total_course = Course.objects.filter(user=user).count()
    total_active_course = Course.objects.filter(user=user, is_active=True).count()
    total_unactive_course = Course.objects.filter(user=user, is_active=False).count()
    total_checking_course = Course.objects.filter(user=user, status="Checking").count()
    my_course_list = Course.objects.filter(user=user).order_by("-id")
    if course_name not in ["", None]:
        my_course_list = my_course_list.filter(title__icontains=course_name)
    if pay_way == "free":
        my_course_list = my_course_list.filter(price=0)
    if pay_way == "unfree":
        my_course_list = my_course_list.filter(price__gt=0)
    my_course_list = paged_items(request, my_course_list)
    return render(request, 'web/auth/course/my_course.html', locals())


def ijoin_activiy(request, uid):
    active_mark = "ijoin_activiy"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    join_act_list = PartActivity.objects.filter(user=user)
    join_act_list = paged_items(request, join_act_list)
    return render(request, 'web/auth/activity/ijoin_activiy.html', locals())


def isponsor_activiy(request, uid):
    active_mark = "isponsor_activiy"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    sponsor_act_list = SponsorActivity.objects.filter(user=user)
    return render(request, 'web/auth/activity/isponsor_activiy.html', locals())


def my_buy_course(request, uid):
    active_mark = "my_buy_course"
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    my_buy_course_list = UserBuyCourse.objects.filter(user__id=uid).order_by("-id")
    for my_buy_course in my_buy_course_list:
        course = Course.objects.filter(id=my_buy_course.course_id).first()
        my_buy_course.course = course
    my_buy_course_list = paged_items(request, my_buy_course_list)
    return render(request, 'web/auth/course/my_buy_course.html', locals())
