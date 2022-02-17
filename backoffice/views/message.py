#encoding=utf-8

import pytz
from django.shortcuts import render, reverse, redirect
from blogs.models import Category
from common.helpers import ok_json, error_json
from django.conf import settings
from django.db.models import F, Q
from ceye_auth.models import User
from django.views.decorators.csrf import csrf_exempt
from backoffice.models import Message
from backoffice.forms.message_form import MessageForm
from backoffice.helper import check_admin_login


@check_admin_login
def back_message_list(request):
    message_list = Message.objects.all().order_by("-id")
    return render(request, 'admin/message/message_list.html', locals())


@csrf_exempt
@check_admin_login
def back_create_message(request):
    if request.method == "GET":
        msg_form = MessageForm(request)
        return render(request, "admin/message/create_message.html", locals())
    if request.method == "POST":
        msg_form = MessageForm(request, request.POST, request.FILES)
        if msg_form.is_valid():
            msg_form.create_message()
            return redirect('back_message_list')
        else:
            error = msg_form.errors
            return render(
                request, "admin/message/create_message.html",
                {
                    'msg_form': msg_form,
                    'error': error
                }
            )


@check_admin_login
def back_delete_message(request, id):
    Message.objects.filter(id=id).delete()
    return redirect('back_message_list')
