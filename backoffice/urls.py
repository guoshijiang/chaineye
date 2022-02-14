from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from backoffice.views.index import back_index
from backoffice.views.user import (
    back_user_list,
    backend_login,
    backend_logout
)
from backoffice.views.index import (
    back_index,
    back_chainsafe
)


urlpatterns: List[Any] = [
    path(r'backend_login', backend_login, name='backend_login'),
    path(r'backend_logout', backend_logout, name='backend_logout'),

    path(r'back_user_list', back_user_list, name='back_user_list'),

    path(r'back_index', back_index, name='back_index'),
    path(r'back_chainsafe', back_chainsafe, name='back_chainsafe'),
]