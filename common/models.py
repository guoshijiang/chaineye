import uuid

from django.db import models


CATE_TYPE_CHOICES = [(x, x) for x in ['Activity', 'Article', 'Question', 'NewsLetter', 'Other']]
BANNER_TYPE_CHOICES = [(x, x) for x in ['Index', 'Activity', 'Other']]


class BaseModel(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    @property
    def UUID(self):
        return uuid.UUID(hex=self.uuid)

    def generate_uuid(self):
        self.uuid = uuid.uuid4().hex

    def save(self, *args, **kw):
        if not self.uuid:
            self.generate_uuid()
        return super(BaseModel, self).save(*args, **kw)


class DecField(models.DecimalField):
    def __init__(self, **kw):
        kw.setdefault('max_digits', 65)
        kw.setdefault('decimal_places', 30)
        super(DecField, self).__init__(**kw)


class IdField(models.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', 100)
        super(IdField, self).__init__(**kwargs)


class Category(BaseModel):
    name = models.CharField('分类名称', max_length=100)
    type = models.CharField(max_length=100, choices=CATE_TYPE_CHOICES, default="Article", db_index=True)
    index = models.IntegerField(default=999, verbose_name='分类排序')
    is_active = models.BooleanField('是否是有效', default=True)

    class Meta:
        verbose_name = '分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type':self.type,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Banner(BaseModel):
    text_info = models.CharField('标题', max_length=50, default='')
    img = models.ImageField('轮播图', upload_to='banner/')
    link_url = models.URLField('图片链接', max_length=100)
    type = models.CharField(max_length=100, choices=BANNER_TYPE_CHOICES, default="Index", db_index=True)
    active = models.CharField('图片状态', max_length=250, default='')
    is_active = models.BooleanField('是否是有效', default=True)

    def __str__(self):
        return self.text_info

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'

    def as_dict(self):
        return {
            'id': self.id,
            'text_info': self.text_info,
            'img': str(self.img),
            'link_url': self.link_url,
            'is_active': self.is_active,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Partner(BaseModel):
    name = models.CharField('名字', max_length=20)
    excerpt = models.TextField('介绍', max_length=200, blank=True)
    img = models.ImageField('图标', upload_to='banner/')
    link_url = models.URLField('网址', max_length=100)
    is_active = models.BooleanField('是否是有效', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合作伙伴'
        verbose_name_plural = '合作伙伴'

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'img': str(self.img),
            'link_url': self.link_url,
            'excerpt': self.excerpt,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Advertise(BaseModel):
    name = models.CharField('名称', max_length=20)
    link_url = models.URLField('网址', max_length=100)
    adv_info = models.CharField('广告信息', max_length=250, default='')
    img = models.ImageField('广告图', upload_to='advertise/')
    is_active = models.BooleanField('是否是有效', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = '广告'

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'link_url': self.link_url,
            'adv_info': self.adv_info,
            'img': str(self.img),
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Asset(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="资产名称",
    )
    chain_name = models.CharField(
        max_length=100, verbose_name="链名称"
    )
    usd_price = DecField(
        max_length=100, verbose_name="美元价格"
    )
    cny_price = DecField(
        max_length=100, verbose_name="人民币价格"
    )
    unit = models.CharField(
        max_length=100, verbose_name="币种精度"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "资产表"
        verbose_name_plural = "资产表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id}
