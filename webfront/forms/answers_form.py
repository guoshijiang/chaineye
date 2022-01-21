#encoding=utf-8

from django import forms
from DjangoUeditor.forms import UEditorField
from question.models import Answers
from mdeditor.fields import MDTextFormField


class AnswersForm(forms.Form):
    content = MDTextFormField()

    class Meta:
        model = Answers
        fields = [
            'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(AnswersForm, self).__init__(*args, **kw)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def create_question(self, question, user):
        Answers.objects.create(
            question=question,
            user=user,
            content=self.clean_content()
        )