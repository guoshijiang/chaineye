#encoding=utf-8


from django import forms
from wallet.models import WalletRecord
from ceye_auth.models import User
from common.models import Asset


class WithdrawForm(forms.ModelForm):
    asset = forms.ModelChoiceField(
        empty_label="请选择提现币种",
        queryset=Asset.objects.filter(is_active=True)
    )
    to_addr = forms.CharField(
        required=True,
        label="提币地址",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入提币地址", "class": "form-control"}
        ),
        error_messages={"required": "请输入提币地址, 提币地址不能为空"},
    )
    amount = forms.CharField(
        required=True,
        label="",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入提币金额", "class": "form-control"}
        ),
        error_messages={"required": "请输入提币金额, 提币金额不能为空"},
    )
    comment = forms.CharField(
        required=False,
        label="提币备注",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入提币备注, 选择输入", "class": "form-control"}
        )
    )

    class Meta:
        model = WalletRecord
        fields = [
            'asset', 'to_addr', 'amount', 'comment'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(WithdrawForm, self).__init__(*args, **kw)

    def clean_asset(self):
        asset = self.cleaned_data.get('asset')
        return asset

    def clean_to_addr(self):
        to_addr = self.cleaned_data.get('to_addr')
        return to_addr

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        return comment

    def create_withdraw(self, user):
        WalletRecord.objects.create(
            user=user,
            asset=self.clean_asset(),
            chain_name="TRON",
            to_addr=self.clean_to_addr(),
            amount=self.clean_amount(),
            comment =self.clean_comment(),
            w_or_d="Withdraw"
        )





