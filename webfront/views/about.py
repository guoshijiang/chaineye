import pytz
from django.shortcuts import render


def about(request):
    nav_mark = "about"
    return render(request, 'web/finance/about.html', locals())

