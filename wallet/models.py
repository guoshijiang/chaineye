# encoding=utf-8
from django.db import models

from common.helpers import d0, dec
from common.models import (
    Asset,
    BaseModel,
    DecField,
)
from ceye_auth.models import User

WithdrawDeposit = [
    (x, x) for x in ["Withdraw", "Deposit", "Transfer"]
]

TransWay = [
    (x, x) for x in ["Input", "Output"]
]

'''
Checking:    审核中(未锁定)
Trading:     交易中 
SendOut:     已发出 
Success:     成功 
Fail:        失败  
CheckPass:   审核通过 
CheckRefuse: 审核拒绝
'''
WalletStatus = [
    (x, x) for x in ["Checking", "Checked", "Trading", "SendOut", "Success", "Fail", "CheckPass", "CheckRefuse"]
]
'''
Input: 收入
Output: 支出
'''
TransRecordStatus = [
    (x, x) for x in ["Output", "Input"]
]


class UserWallet(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="user_wallet_rel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="user_wallet_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    chain_name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="链名称",
    )
    address = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="地址",
    )
    balance = DecField(
        default=d0,
        verbose_name="钱包余额"
    )
    in_amount = DecField(
        default=d0,
        verbose_name="钱包入账"
    )
    out_amount = DecField(
        default=d0,
        verbose_name="钱包出账"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "用户钱包表"
        verbose_name_plural = "用户钱包表"

    def __str__(self):
        return self.address

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }


class WalletRecord(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="wallet_record_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="wallet_record_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    chain_name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="链名称",
    )
    from_addr = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="转出地址",
    )
    to_addr = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="转入地址",
    )
    amount = DecField(
        default=d0,
        verbose_name="转账金额"
    )
    tx_fee = DecField(
        default=d0,
        verbose_name="转账手续费"
    )
    tx_hash = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="交易Hash",
    )
    comment = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="备注",
    )
    w_or_d = models.CharField(
        max_length=100,
        choices=WithdrawDeposit,
        default="Withdraw",
        verbose_name="充值提现",
    )
    status = models.CharField(
        max_length=100,
        choices=WalletStatus,
        default="Checked",
        verbose_name="状态",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "钱包充值提现记录表"
        verbose_name_plural = "钱包充值提现记录表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class TansRecord(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="trans_relate_record_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="trans_relate_record_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    amount = DecField(
        default=d0,
        verbose_name="金额"
    )
    trans_way = models.CharField(
        max_length=100,
        choices=TransWay,
        default="Input",
        verbose_name="收入支出",
    )
    source = models.CharField(
        max_length=1280,
        default="",
        blank=True,
        null=True,
        verbose_name="支付收入来源",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "钱包交易记录表"
        verbose_name_plural = "钱包交易记录表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}
