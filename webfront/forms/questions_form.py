#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from question.models import Questions, Category
from mdeditor.fields import MDTextFormField


class QuestionsForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="问题标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入问题标题"}
        ),
        error_messages={"required": "请输入问题标题, 问题标题不能为空"},
    )
    category = forms.ModelChoiceField(
        empty_label="请选择问题类别",
        queryset=Category.objects.filter(type="Question", is_active=True)
    )
    content = MDTextFormField()

    class Meta:
        model = Questions
        fields = [
            'title', 'category', 'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(QuestionsForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            return self.add_error('title', '标题不能为空')
        return title

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category in ['', None]:
            return self.add_error('title', '分类必须要选择')
        return category

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        return excerpt

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def create_question(self, user):
        Questions.objects.create(
            title=self.clean_title(),
            category=self.clean_category(),
            user=user,
            content=self.clean_content()
        )





