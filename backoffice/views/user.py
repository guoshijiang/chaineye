# encoding=utf-8

from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ceye_auth.models import (
    User,
    Account
)
from backoffice.forms.login_form import AccountLoginForm
from backoffice.helper import check_admin_login


@csrf_exempt
def backend_login(request):
    if request.method == "GET":
        login_form = AccountLoginForm(request)
        return render(request, "admin/auth/login.html", locals())
    elif request.method == "POST":
        login_form = AccountLoginForm(request, request.POST)
        if login_form.is_valid():
            user_name = login_form.clean_user_name()
            user = Account.objects.filter(name=user_name).first()
            request.session["backend_is_login"] = True
            request.session["b_user_id"] = user.id
            request.session["b_user_name"] = user.name
            request.session["b_role"] = user.role
            user.online = "Yes"
            user.save()
            return redirect("back_index")
        else:
            error = login_form.errors
            return render(
                request, 'admin/auth/login.html',
                {'login_form': login_form, 'error': error}
            )


@csrf_exempt
@check_admin_login
def backend_logout(request):
    request.session["backend_is_login"] = False
    request.session.flush()
    return redirect("backend_login")


@csrf_exempt
@check_admin_login
def back_user_list(request):
    b_user_list = User.objects.all().order_by("-id")
    b_user_list = paged_items(request, b_user_list)
    return render(request, 'admin/user/user_list.html', locals())