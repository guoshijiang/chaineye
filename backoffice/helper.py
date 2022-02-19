# encoding=utf-8

import json
from django.shortcuts import redirect


def check_admin_login(func):
    def user_auth(request, *args, **kwargs):
        if request.session.get("backend_is_login") is False \
                or request.session.get("backend_is_login") is None:
            return redirect("backend_login")
        return func(request, *args, **kwargs)
    return user_auth


def check_bearer_auth(func):
    def check_bearer_auth(request, *args, **kwargs):
        if settings.API_TOKEN:
            auth = request.META.get('HTTP_AUTHORIZATION')
            if auth != 'Bearer {}'.format(settings.API_TOKEN):
                return error_json("Monitor token is error", 1000)
        return func(request, *args, **kwargs)
    return check_bearer_auth
