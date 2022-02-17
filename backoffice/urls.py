from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from backoffice.views.index import back_index
from backoffice.views.user import (
    back_user_list,
    backend_login,
    backend_logout,
    back_user_wallet
)
from backoffice.views.index import (
    back_index,
    back_blog_check,
    back_chainsafe,
    back_chainsafe_check,
    back_question_list,
    back_question_check,
    back_activity_list,
    back_activity_check
)

from backoffice.views.course import (
    back_course_list,
    back_course_check,
    back_course_artcle,
    back_course_article_check,
    back_course_comment,
    course_comment_check
)
from backoffice.views.message import (
    back_message_list,
    back_create_message,
    back_delete_message
)
from backoffice.views.channel_api import (
    get_chainsafe,
    get_blogs,
    get_course
)


urlpatterns: List[Any] = [
    path(r'backend_login', backend_login, name='backend_login'),
    path(r'backend_logout', backend_logout, name='backend_logout'),
    path(r'back_user_list', back_user_list, name='back_user_list'),
    path(r'<int:uid>/back_user_wallet', back_user_wallet, name='back_user_wallet'),

    path(r'back_index', back_index, name='back_index'),
    path(r'<int:bid>/back_blog_check', back_blog_check, name='back_blog_check'),
    path(r'back_chainsafe', back_chainsafe, name='back_chainsafe'),
    path(r'<int:id>/back_chainsafe_check', back_chainsafe_check, name='back_chainsafe_check'),
    path(r'back_question_list', back_question_list, name='back_question_list'),
    path(r'<int:id>/back_question_check', back_question_check, name='back_question_check'),
    path(r'back_activity_list', back_activity_list, name='back_activity_list'),
    path(r'<int:id>/back_activity_check', back_activity_check, name='back_activity_check'),

    path(r'back_course_list', back_course_list, name='back_course_list'),
    path(r'<int:cid>/back_course_check', back_course_check, name='back_course_check'),
    path(r'<int:cid>/back_course_artcle', back_course_artcle, name='back_course_artcle'),
    path(r'<int:caid>/back_course_article_check', back_course_article_check, name='back_course_article_check'),
    path(r'<int:aid>/back_course_comment', back_course_comment, name='back_course_comment'),
    path(r'<int:cid>/course_comment_check', course_comment_check, name='course_comment_check'),

    path(r'back_message_list', back_message_list, name='back_message_list'),
    path(r'back_create_message', back_create_message, name='back_create_message'),
    path(r'<int:id>/back_delete_message', back_delete_message, name='back_delete_message'),

    path(r'get_chainsafe', get_chainsafe, name='get_chainsafe'),
    path(r'get_blogs', get_blogs, name='get_blogs'),
    path(r'get_course', get_course, name='get_course'),
]