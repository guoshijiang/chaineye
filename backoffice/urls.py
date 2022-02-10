from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from backoffice.views.index import back_index
from backoffice.views.user import back_user_list


urlpatterns: List[Any] = [
    path(r'back_user_list', back_user_list, name='back_user_list'),
]