#encoding=utf-8

from django.conf import settings
from django.http import HttpResponse

def access_token_required(func):
    def __w(request, *args, **kw):
        access_token =  request.GET.get('access_token')
        if settings.ACCESS_TOKEN and settings.ACCESS_TOKEN != access_token:
            return HttpResponse('access token is invalid')
        return func(request, *args, **kw)

    return __w

