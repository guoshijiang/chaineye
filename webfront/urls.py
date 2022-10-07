from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from webfront.views.blog import (
    index, article_list, tag_list, arctle_detail, blog_list
)
from webfront.views.about import about
from webfront.views.activity import (
    activity,
    activity_detail,
    participate_act,
    sponsor_act,
    publish_activity,
    update_activity
)
from webfront.views.auth import (
    sms_send,
    sms_check,
    register,
    login_by_verify_code,
    login_by_verify_passwd,
    my,
    logout,
    my_article,
    my_activity,
    update_user_info,
    create_article,
    update_article,
    my_questions,
    my_wallet,
    my_course,
    ijoin_activiy,
    isponsor_activiy,
    my_buy_course
)
from webfront.views.planet import (
    plannet_course,
    course_detail,
    course_article_detail,
    create_course,
    update_course,
    create_course_article,
    wirte_course_article
)
from webfront.views.chain_safe import (
    chain_safe,
    chain_safe_detail
)
from webfront.views.questions import (
    questions,
    create_answer,
    create_question,
    question_detail
)
from webfront.views.wallet import (
    wallet_withdraw,
    wallet_record,
    income_record,
    trans_record,
)
from webfront.views.wallet_chain import withdraw_deposit_notify
from webfront.views.newsletter import (
    newsletter,
    newsbad,
    newsgood,
    newsletter_detail
)

urlpatterns: List[Any] = [
    path(r'', index, name='index'),

    # 文章模块
    path(r'blog_list', blog_list, name='blog_list'),
    path(r'article_list', article_list, name='article_list'),
    path(r'<str:tag>/tag_list', tag_list, name='tag_list'),
    path(r'arctle_detail', arctle_detail, name='arctle_detail'),

    # 问答
    path(r'questions', questions, name='questions'),
    path(r'<int:qs_id>/question_detail', question_detail, name='question_detail'),
    path(r'<int:ans_id>/create_answer', create_answer, name='create_answer'),
    path(r'<int:uid>/create_question', create_question, name='create_question'),

    # 活动
    path(r'activity', activity, name='activity'),
    path(r'<int:id>/participate_act', participate_act, name='participate_act'),
    path(r'<int:id>/sponsor_act', sponsor_act, name='sponsor_act'),
    path(r'<int:id>/activity_detail', activity_detail, name='activity_detail'),
    path(r'<int:uid>/publish_activity', publish_activity, name='publish_activity'),
    path(r'<int:act_id>/update_activity', update_activity, name='update_activity'),

    # 链安
    path(r'chain_safe', chain_safe, name='chain_safe'),
    path(r'<int:cid>/chain_safe_detail', chain_safe_detail, name='chain_safe_detail'),

    # 专栏课程
    path(r'plannet_course', plannet_course, name='plannet_course'),
    path(r'<int:cid>/course_detail', course_detail, name='course_detail'),
    path(r'<int:arcticle_id>/course_article_detail', course_article_detail, name='course_article_detail'),
    path(r'<int:uid>/create_course', create_course, name='create_course'),
    path(r'<int:cid>/update_course', update_course, name='update_course'),
    path(r'<int:cid>/create_course_article', create_course_article, name='create_course_article'),
    path(r'<int:act_id>/wirte_course_article', wirte_course_article, name='wirte_course_article'),

    # 用户
    path(r'sms_send', sms_send, name='sms_send'),
    path(r'sms_check', sms_check, name='sms_check'),
    path(r'register', register, name='register'),
    path(r'login_by_verify_code', login_by_verify_code, name='login_by_verify_code'),
    path(r'login_by_verify_passwd', login_by_verify_passwd, name='login_by_verify_passwd'),
    path(r'<int:uid>/my', my, name='my'),
    path(r'<int:uid>/my_article', my_article, name='my_article'),
    path(r'<int:uid>/my_activity', my_activity, name='my_activity'),
    path(r'<int:uid>/update_user_info', update_user_info, name='update_user_info'),
    path(r'<int:uid>/create_article', create_article, name='create_article'),
    path(r'<int:arc_id>/update_article', update_article, name='update_article'),
    path(r'<int:uid>/my_questions', my_questions, name='my_questions'),
    path(r'<int:uid>/my_wallet', my_wallet, name='my_wallet'),
    path(r'<int:uid>/my_course', my_course, name='my_course'),
    path(r'<int:uid>/ijoin_activiy', ijoin_activiy, name='ijoin_activiy'),
    path(r'<int:uid>/isponsor_activiy', isponsor_activiy, name='isponsor_activiy'),
    path(r'<int:uid>/my_buy_course', my_buy_course, name='my_buy_course'),
    path(r'logout', logout, name='logout'),

    # wallet module
    path(r'wallet_withdraw', wallet_withdraw, name='wallet_withdraw'),
    path(r'wallet_record', wallet_record, name='wallet_record'),
    path(r'income_record', income_record, name='income_record'),
    path(r'trans_record', trans_record, name='trans_record'),

    # 充值提现通知
    path(r'withdraw_deposit_notify', withdraw_deposit_notify, name='withdraw_deposit_notify'),

    # 行业资讯
    path(r'newsletter', newsletter, name='newsletter'),
    path(r'newsbad', newsbad, name='newsbad'),
    path(r'newsgood', newsgood, name='newsgood'),
    path(r'<int:id>/newsletter_detail', newsletter_detail, name='newsletter_detail'),

    # 关于我们
    path(r'about', about, name='about'),
]