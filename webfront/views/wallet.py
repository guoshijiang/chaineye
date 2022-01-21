#encoding=utf-8


from django.shortcuts import render, redirect
from wallet.models import WalletRecord, TansRecord, UserWallet
from ceye_auth.models import User, UserInfo
from wallet.forms.withdraw_form import WithdrawForm
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt


def income_record(request):
    tab = "income"
    nav_mark = "my_wallet"
    uid = request.session.get("user_id")
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    input_trans_list = TansRecord.objects.filter(
        user__id=uid,
        trans_way="Input",
        is_active=True
    )
    input_trans_list = paged_items(request, input_trans_list)
    return render(request, 'web/auth/wallet/income_record.html', locals())


def trans_record(request):
    tab = "trans"
    nav_mark = "my_wallet"
    uid = request.session.get("user_id")
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    trans_list = TansRecord.objects.filter(user__id=uid, is_active=True)
    trans_list = paged_items(request, trans_list)
    return render(request, 'web/auth/wallet/trans_record.html', locals())


def wallet_record(request):
    tab = "wallet_record"
    nav_mark = "my_wallet"
    uid = request.session.get("user_id")
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    w_record_list = WalletRecord.objects.filter(user__id=uid, is_active=True)
    w_record_list = paged_items(request, w_record_list)
    return render(request, 'web/auth/wallet/wallet_record.html', locals())


@csrf_exempt
def wallet_withdraw(request):
    tab = "withdraw"
    nav_mark = "my_wallet"
    uid = request.session.get("user_id")
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    user_wallet = UserWallet.objects.filter(user__id=uid).first()
    if request.method == 'GET':
        w_form = WithdrawForm(request)
        return render(request, 'web/auth/wallet/withdraw.html', locals())
    elif request.method == 'POST':
        w_form = WithdrawForm(request, request.POST)
        if w_form.is_valid():
            w_form.create_withdraw(user)
            return redirect('wallet_record')
        else:
            error = w_form.errors
            return render(
                request, "web/auth/wallet/withdraw.html",
                {
                    'w_form': w_form,
                    'error': error
                }
            )

