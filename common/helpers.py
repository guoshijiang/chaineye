#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import functools
import hashlib
import hmac
import logging
import sys
import time
from bisect import bisect

from datetime import datetime, timezone
from decimal import ROUND_FLOOR, ROUND_UP
from decimal import Context as DecimalContext
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote_plus, urlencode

import pytz
import requests
from django.conf import settings
from django.core.paginator import EmptyPage
from django.http import HttpRequest, JsonResponse
from django.utils.timezone import localtime, now

from common.paginator import MyPaginator

import json
import uuid


def getLogger(name):
    logger = logging.getLogger(name)
    if len(sys.argv) > 1 and sys.argv[-1] == "test":
        logger.disabled = True
    return logger


def get_hostname() -> str:
    import socket
    return socket.gethostname()


def get_processid() -> int:
    import os
    return os.getpid()


def make_timestamp() -> float:
    return time.time() * 1000


def time_to_str(time_time: Optional[float] = None, tz: str = "Asia/Shanghai") -> str:
    time_time = time_time or time.time()
    dt = datetime.fromtimestamp(time_time).astimezone(pytz.timezone(tz))
    return str(dt)


def ok_json(data: Any, code: int = 200) -> JsonResponse:
    return JsonResponse({"ok": True, "code": code, "result": data})


def keep_two_place(value):
    if not value:
        return "0"
    dec_value = Decimal(value).quantize(Decimal("0.00"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )


def error_json(msg: str, code: int = -1, status: int = 200) -> JsonResponse:
    return JsonResponse({"ok": False, "code": code, "msg": msg, }, status=status)


def floor_decimal(amount: Decimal, digits: int = 18) -> Decimal:
    return amount.quantize(
        Decimal("1E-%d" % digits), context=DecimalContext(prec=60, rounding=ROUND_FLOOR)
    )


def up_decimal(amount: Decimal, digits: int = 18) -> Decimal:
    return amount.quantize(
        Decimal("1E-%d" % digits), context=DecimalContext(prec=60, rounding=ROUND_UP)
    )


def round_decimal(amount: Decimal, digits: int = 18) -> Decimal:
    return amount.quantize(Decimal("1E-%d" % digits), context=DecimalContext(prec=60))


limit_steps: List[int] = [5, 10, 20, 50, 100, 500, 1000, 5000]


def search_limit(limit: int) -> int:
    limit = max(0, min(limit, 5000))
    return limit_steps[bisect(limit_steps, limit)]


def dec(value: Any, default: Any = "0", digits: int = 18) -> Decimal:
    try:
        # if isinstance(value, float):
        #    value = str(value)
        if isinstance(value, Decimal):
            return floor_decimal(value, digits=digits)
        else:
            return floor_decimal(Decimal(value), digits=digits)
    except (InvalidOperation, TypeError):
        return Decimal(default)


parse_decimal = dec
d0: Decimal = dec("0")
d1 = dec("1")
d2 = dec("2")
d10 = dec("10")
d100 = dec("100")
d200 = dec("200")
d1000 = dec("1000")
d1_000 = dec("1000")
d1k = d1000
d10000 = dec("10000")
d10_000 = dec("10000")
d1m = dec("1_000_000")


def dec05up(a: Decimal) -> Decimal:
    half = dec("0.5", digits=1)
    floored = up_decimal(a + a, digits=0)
    return floored * half


def dec05floor(a: Decimal) -> Decimal:
    half = dec("0.5", digits=1)
    floored = floor_decimal(a + a, digits=0)
    return floored * half


dec05 = dec05floor


def mod_decimal(amount: Decimal, div: Decimal) -> Tuple[Decimal, Decimal]:
    divided = floor_decimal(amount / div, digits=0) * div
    remainder = amount - divided
    return divided, remainder


def _xx_decprice(value: Any) -> Decimal:
    return dec(value, digits=6)


decprice = dec


def decstr(value: Union[Decimal, float], round_number=None) -> str:
    if isinstance(value, float):
        value = Decimal(value)
    if round_number is not None:
        _s = "0."
        for i in range(round_number):
            _s += "0"
        value = value.quantize(Decimal(_s))

    s = "{:f}".format(value)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s


MIN = dec("0", digits=8)


def parse_int(v, default=0):
    try:
        v = int(v)
    except (ValueError, TypeError) as e:
        v = default
    return v


def get_page(request: HttpRequest) -> int:
    page = parse_int(request.GET.get("page", 1), 1)
    if page < 1:
        page = 1
    return page


PAGE_SIZE = 20


def paged_items(request: HttpRequest, qs, pagesize=PAGE_SIZE, page_cls=MyPaginator):
    paginator = page_cls(qs, pagesize, adjacent_pages=3)
    page = get_page(request)
    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    args = {}
    for key, value in request.GET.items():
        if key != "page":
            args[key] = value.encode("utf-8")

    if len(args) == 0:
        items.prefix_uri = request.path + "?"
    else:
        items.prefix_uri = request.path + "?" + urlencode(args) + "&"
    return items


def sleep(sleep_time: float) -> None:
    time.sleep(sleep_time)


def utc_now() -> datetime:
    return now()


def current_now() -> datetime:
    return localtime(utc_now())


def timestamp_to_utc(time_stamp):
    return datetime.utcfromtimestamp(time_stamp)


def retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(3):
            r = func(*args, **kwargs)
            if r:
                return r
            else:
                time.sleep(1)

    return wrapper


def datetime2utctimestamp(datetime):
    timestamp = datetime.replace(tzinfo=timezone.utc).timestamp()
    return timestamp



def check_bearer_auth(func):
    def check_bearer_auth(request, *args, **kwargs):
        if settings.API_TOKEN:
            auth = request.META.get('HTTP_AUTHORIZATION')
            if auth != 'Bearer {}'.format(settings.API_TOKEN):
                return error_json("Monitor token is error", 1000)
        return func(request, *args, **kwargs)
    return check_bearer_auth

