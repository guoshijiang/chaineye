#encoding=utf-8

import pytz
import markdown
from django.shortcuts import render
from question.models import (
    Answers, Questions,
)
from blogs.models import Category
from django.shortcuts import reverse, redirect
from common.helpers import ok_json, error_json, paged_items
from django.conf import settings
from django.db.models import F, Q
from webfront.forms.questions_form import QuestionsForm
from webfront.forms.answers_form import AnswersForm
from ceye_auth.models import UserInfo, User


tz = pytz.timezone(settings.TIME_ZONE)


def questions(request):
    cat_id = int(request.GET.get('cat_id', 0))
    cat_name = request.GET.get('cat_name', "")
    page = int(request.GET.get('page', 0))
    page_size = int(request.GET.get('page_size', 10))
    start = page * page_size
    end = start + page_size
    nav_mark = "questions"
    question_cat_list = Category.objects.filter(
        type='Question',
        is_active=True
    ).order_by("id").all()
    question_cat = Category.objects.filter(id=cat_id).order_by("-id").first()
    if cat_id not in ["0", 0, None]:
        question_list = Questions.objects.filter(category=question_cat).order_by('-id')
    else:
        question_list = Questions.objects.all().order_by('-id')
    if request.is_ajax():
        if cat_id not in ["0", 0, None]:
            question_list = Questions.objects.filter(category=question_cat).order_by('-id')[start:end]
        else:
            question_list = Questions.objects.all().order_by('-id')[start:end]
        ret_question_list = []
        ret_category_list = []
        total = len(question_list)
        for ns_lt in question_list:
            created_at = ns_lt.created_at.astimezone(tz).strftime('%m月%d日 %H:%M')
            question_json = {
                "id": ns_lt.id,
                "title": ns_lt.title,
                "content": ns_lt.content,
                'good': ns_lt.good,
                'bad': ns_lt.bad,
                'created_at': created_at,
            }
            ret_question_list.append(question_json)
        for question_cat in question_cat_list:
            cat_json = {
                "id": question_cat.id,
                "cat_name": question_cat.name,
            }
            ret_category_list.append(cat_json)
        ret_data = {
            "category": ret_category_list,
            "question": {
                "total": total,
                "data": ret_question_list
            }
        }
        return ok_json(ret_data)
    else:
        for question in question_list:
            question.content = markdown.markdown(
                question.content,
                extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                ]
            )
        question_list = paged_items(request, question_list)
        return render(request, 'web/questions/questions.html', locals())


def question_detail(request, qs_id):
    nav_mark = "questions"
    question = Questions.objects.filter(id=qs_id).order_by("-id").first()
    user_if = UserInfo.objects.filter(id=question.user.id).first()
    question.user.photo = user_if.photo
    question.content = markdown.markdown(
        question.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    question.views += 1
    question.save()
    qs_answer_list = Answers.objects.filter(question=question).order_by("-id")
    for qs_answer in qs_answer_list:
        qs_answer.content = markdown.markdown(
            qs_answer.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
    len_answer = len(qs_answer_list)
    if request.is_ajax():
        qs_answer_ret = []
        for qs_answer in qs_answer_list:
            qs_answer_ret.append(qs_answer.as_dict())
        return ok_json(qs_answer_ret)
    else:
        if request.method == 'GET':
            answer_form = AnswersForm(request)
            return render(request, 'web/questions/question_detail.html', locals())
        if request.method == 'POST':
            answer_form = AnswersForm(request, request.POST)
            return render(request, 'web/questions/question_detail.html', locals())


def create_question(request, uid):
    nav_mark = "questions"
    user = User.objects.filter(id=uid).first()
    if request.method == 'GET':
        qs_form = QuestionsForm(request)
        return render(request, 'web/questions/create_question.html', locals())
    elif request.method == 'POST':
        qs_form = QuestionsForm(request, request.POST)
        if qs_form.is_valid():
            qs_form.create_question(user)
            return redirect('questions')
        else:
            error = qs_form.errors
            return render(
                request, "web/questions/create_question.html",
                {
                    "user_id": uid,
                    'qs_form': qs_form,
                    'error': error
                }
            )

def create_answer(request, ans_id):
    nav_mark = "questions"
    question = Questions.objects.filter(id=ans_id).first()
    question.answers += 1
    question.save()
    if request.method == 'GET':
        answer_form = AnswersForm(request)
        return render(request, 'web/questions/questions.html', locals())
    elif request.method == 'POST':
        answer_form = AnswersForm(request, request.POST)
        if answer_form.is_valid():
            answer_form.create_question(question, question.user)
            return redirect('question_detail', question.id)
        else:
            error = answer_form.errors
            return render(
                request, "web/questions/questions.html",
                {
                    "ans_id": ans_id,
                    'answer_form': answer_form,
                    'error': error
                }
            )

