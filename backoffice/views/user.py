# encoding=utf-8

from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ceye_auth.models import (
    User
)


def back_user_list(request):
    b_user_list = User.objects.all().order_by("-id")
    b_user_list = paged_items(request, b_user_list)
    return render(request, 'admin/user/user_list.html', locals())