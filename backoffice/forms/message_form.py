# encoding=utf-8

from django import forms
from backoffice.models import Message
from DjangoUeditor.forms import UEditorField


class MessageForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "text", "placeholder": "请输入用户名", "class": "form-control"}
        ),
        error_messages={"required": "请输入, 用户名不能为空"},
    )
    img = forms.ImageField(
        required=True,
        error_messages={"invalid": "请上传图片, 图片不能为空"},
    )
    content = UEditorField(
        label='活动内容',
        width=960, height=900,
        toolbars="full",
        imagePath="upimg/",
        filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}
    )

    def __init__(self, request, *args, **kw):
        self.request = request
        super(MessageForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('活动标题不能为空')
        return title

    def clean_img(self):
        img = self.cleaned_data.get('img')
        return img

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content in ['', None]:
            raise forms.ValidationError('文章内容不能为空')
        return content

    def create_message(self):
        Message.objects.create(
            title=self.clean_title(),
            img=self.clean_img(),
            content=self.clean_content()
        )