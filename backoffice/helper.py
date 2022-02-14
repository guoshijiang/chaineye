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