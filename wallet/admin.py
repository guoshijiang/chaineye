#encoding=utf-8

from django.contrib import admin
from wallet.models import (
    UserWallet, WalletRecord, TansRecord
)

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'chain_name', 'created_at')


@admin.register(WalletRecord)
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


@admin.register(TansRecord)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')





