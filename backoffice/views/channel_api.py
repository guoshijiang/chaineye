#encoding=utf-8

import pytz
from django.shortcuts import render, reverse, redirect
from common.helpers import ok_json, error_json
from django.conf import settings
from django.db.models import F, Q
from ceye_auth.models import User
from django.views.decorators.csrf import csrf_exempt
from blogs.models import Article, ChainSafe


def get_chainsafe():
    return ok_json("")


def get_blogs():
    return ok_json("")


def get_course():
    return ok_json("")
