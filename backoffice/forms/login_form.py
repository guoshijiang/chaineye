# encoding=utf-8

from django import forms
from ceye_auth.models import Account
from ceye_auth.helper import hash_code


class AccountLoginForm(forms.Form):
    user_name = forms.CharField(
        required=True,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "text", "placeholder": "请输入用户名", "class": "form-control"}
        ),
        error_messages={"required": "请输入, 用户名不能为空"},
    )
    password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入密码", "class": "form-control"}
        ),
        error_messages={"required": "请输入密码, 密码不能为空"},
    )

    def __init__(self, request, *args, **kw):
        self.request = request
        super(AccountLoginForm, self).__init__(*args, **kw)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name in ["", None]:
            raise forms.ValidationError('用户名字不能为空')
        return user_name

    def clean_password(self):
        user = Account.objects.filter(name=self.cleaned_data.get('user_name')).first()
        if user is None:
            raise forms.ValidationError('用户不存在')
        password = self.cleaned_data.get('password')
        if password in ["", None]:
            raise forms.ValidationError('密码不能为空')
        if user.password != password:
            raise forms.ValidationError('密码错误，请核对之后输入')
        return password