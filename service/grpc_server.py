#encoding=utf-8

import pytz
from service.savourrpc import chaineye_pb2, common_pb2, chaineye_pb2_grpc
from django.conf import settings
from typing import Dict, List, Sequence, Tuple
from blogs.models import Article, ChainSafe, Category
from ceye_auth.models import User
from wallet.models import UserWallet, WalletRecord, Asset
from common.helpers import dec
from newsletter.models import Newsletter


tz = pytz.timezone(settings.TIME_ZONE)


class ChaineyeServer(chaineye_pb2_grpc.ChaineyeServiceServicer):
    def getArticleCat(self, request, context)->chaineye_pb2.ArticleCatRep:
        type = int(request.type)
        cat_return_list: List[chaineye_pb2.CatList] = []
        if type == 0:
            cat_list = Category.objects.filter(is_active=True).order_by("id")
            for cat in cat_list:
                item = chaineye_pb2.CatList (
                    id=str(cat.id),
                    name=cat.name
                )
                cat_return_list.append(item)
            return chaineye_pb2.ArticleCatRep(
                code=common_pb2.SUCCESS,
                msg="get article success",
                cat_list=cat_return_list
            )
        if type == 1:
            item = chaineye_pb2.CatList(
                id=str(1),
                name="安全"
            )
            cat_return_list.append(item)
            return chaineye_pb2.ArticleCatRep(
                code=common_pb2.SUCCESS,
                msg="get article success",
                cat_list=cat_return_list
            )

    def getArticleList(self, request, context) -> chaineye_pb2.ArticleListRep:
        type = int(request.type)
        cat_id = int(request.cat_id)
        page = request.page - 1
        pagesize = request.pagesize
        start = page * pagesize
        end = start + pagesize
        blog_return_list: List[chaineye_pb2.ArticleList] = []
        if type == 0:
            if cat_id == 0:
                blog_lists = Article.objects.all().order_by("-id")
                blog_list = blog_lists[start:end]
            else:
                blog_lists = Article.objects.filter(category__id=cat_id).order_by("-id")[start:end]
                blog_list = blog_lists[start:end]
            for blog in blog_list:
                item = chaineye_pb2.ArticleList(
                    id=str(blog.id),
                    title=blog.title,
                    abstract=blog.excerpt,
                    type=type,
                    author=blog.user.user_name,
                    views=blog.views,
                    add_time=blog.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                    upd_time=blog.updated_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                    cover=str(blog.img),
                    like=blog.likes
                )
                blog_return_list.append(item)
            return chaineye_pb2.ArticleListRep(
                code=common_pb2.SUCCESS,
                msg="get article success",
                total=len(blog_lists),
                articles=blog_return_list
            )
        elif type == 1:
            chain_safe_lists = ChainSafe.objects.all().order_by("-id")
            chain_safe_list = chain_safe_lists[start:end]
            for chain_safe in chain_safe_list:
                item = chaineye_pb2.ArticleList(
                    id=str(chain_safe.id),
                    title=chain_safe.title,
                    abstract=chain_safe.excerpt,
                    type=type,
                    author=chain_safe.author,
                    views=chain_safe.views,
                    add_time=chain_safe.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                    upd_time=chain_safe.updated_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                    cover=str(chain_safe.img),
                    like=chain_safe.likes,
                )
                blog_return_list.append(item)
            return chaineye_pb2.ArticleListRep(
                code=common_pb2.SUCCESS,
                msg="get article success",
                total=len(chain_safe_lists),
                articles=blog_return_list
            )
        else:
            news_letter_lists = Newsletter.objects.all().order_by("-id")
            news_letter_list = news_letter_lists[start:end]
            for news_letter in news_letter_list:
                item = chaineye_pb2.ArticleList(
                    id=str(news_letter.id),
                    title=news_letter.title,
                    abstract=news_letter.excerpt,
                    type=type,
                    author=news_letter.user.user_name,
                    views=news_letter.views,
                    add_time=news_letter.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                    upd_time=news_letter.updated_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                    cover=str(news_letter.img),
                    like=news_letter.good + news_letter.bad,
                )
                blog_return_list.append(item)
            return chaineye_pb2.ArticleListRep(
                code=common_pb2.SUCCESS,
                msg="get article success",
                total=len(news_letter_lists),
                articles=blog_return_list
            )


    def getArticleDetail(self, request, context) -> chaineye_pb2.ArticleDetailRep:
        type = request.type
        id = int(request.id)
        if type == 0:
            blog = Article.objects.filter(id=id).first()
            return chaineye_pb2.ArticleDetailRep(
                code=common_pb2.SUCCESS,
                msg="get article detail success",
                title=blog.title,
                detail=blog.body,
                author_id=str(blog.user.id),
                author=blog.user.user_name,
                views=blog.views,
                add_time=blog.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                upd_time=blog.updated_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                like=blog.likes,
                comments=None,
                likes=None
            )
        elif type == 1:
            chain_safe = ChainSafe.objects.filter(id=id).first()
            return chaineye_pb2.ArticleDetailRep(
                code=common_pb2.SUCCESS,
                msg="get article detail success",
                title=chain_safe.title,
                detail=chain_safe.body,
                author_id=str(0),
                author=chain_safe.author,
                views=chain_safe.views,
                add_time=chain_safe.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                upd_time=chain_safe.updated_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                like=chain_safe.likes,
                comments=None,
                likes=None
            )
        else:
            news_letter = Newsletter.objects.objects.filter(id=id).first()
            return chaineye_pb2.ArticleDetailRep(
                code=common_pb2.SUCCESS,
                msg="get article detail success",
                title=news_letter.title,
                detail=news_letter.content,
                author_id=str(news_letter.user.id),
                author=news_letter.user.user_name,
                views=news_letter.views,
                add_time=news_letter.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                upd_time=news_letter.updated_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                like=news_letter.good + news_letter.bad,
                comments=None,
                likes=None
            )


    def getCommentList(self, request, context)->chaineye_pb2.CommentListRep:
        return chaineye_pb2.CommentListRep(
            code=common_pb2.ERROR,
            msg="this rpc current not support"
        )


    def getLikeAddress(self, request, context) -> chaineye_pb2.AddressRep:
        wallet_return_data: List[chaineye_pb2.AssetAddress] = []
        author_id = int(request.author_id)
        user_wallets = UserWallet.objects.filter(user__id=author_id).order_by("-id")
        for uw in user_wallets:
            uw_item = chaineye_pb2.AssetAddress(
                asset=uw.asset.name,
                address=uw.address
            )
            wallet_return_data.append(uw_item)
        return chaineye_pb2.AddressRep (
            code=common_pb2.SUCCESS,
            msg="get like address success",
            asset_address=wallet_return_data
       )

    def likeArticle(self, request, context):
        tx_hash = request.tx_hash
        like_from = request.like_from
        like_to = request.like_to
        amount = request.amount
        asset_name = request.asset_name
        token_address = request.token_address
        author_id = int(request.author_id)
        asset_db = Asset.objects.filter(name=asset_name).first()
        if asset_db is None:
            return chaineye_pb2.LikeRep(
                code=common_pb2.ERROR,
                msg="do not support this asset",
            )
        user = User.objects.get(id=author_id)
        if user is None:
            return chaineye_pb2.LikeRep(
                code=common_pb2.ERROR,
                msg="user is not exist",
            )
        user_wallets = UserWallet.objects.filter(user=user, asset__name=asset_name).first()
        if user_wallets is not None:
            user_wallets.balance += dec(amount)
            user_wallets.in_amount += dec(amount)
            WalletRecord.objects.create(
                user=user,
                asset=asset_db,
                chain_name="unknown",
                from_addr=like_from,
                to_addr=token_address + like_to,
                amount=amount,
                tx_hash=tx_hash,
                comment="赞赏收入",
                w_or_d="Like",
                status="Checked",
                is_active=True
            )
            return chaineye_pb2.LikeRep(
                code=common_pb2.SUCCESS,
                msg="like success",
            )
        else:
            return chaineye_pb2.LikeRep(
                code=common_pb2.ERROR,
                msg="use wallet is not exist",
            )
