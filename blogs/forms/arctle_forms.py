#encoding=utf-8


from django import forms
from blogs.models import Tag, Category, Article
from mdeditor.fields import MDTextFormField
from django.core.files.base import ContentFile
from ceye_auth.models import User


class ArtcleForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="文章标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入文章标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入文章标题, 文章标题不能为空"},
    )
    body = MDTextFormField()
    excerpt =forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'style': 'height:200px; width:100%;outline: none;padding: 15px;box-sizing: border-box;',
                'placeholder': '请输入文章摘要'
            }
        )
    )
    category = forms.ModelChoiceField(
        empty_label="请选择文章类别",
        queryset=Category.objects.filter(type="Article", is_active=True)
    )
    img = forms.ImageField(
        required=False,
        error_messages={"invalid": "请上传图片, 图片不能为空"},
    )

    class Meta:
        model = Article
        fields = [
            'title', 'body', 'excerpt', 'category', 'img'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(ArtcleForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('文章标题不能为空')
        return title

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body in ['', None]:
            raise forms.ValidationError('文章内容不能为空')
        return body

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt in ['', None]:
            raise forms.ValidationError('文章zhaiyi不能为空')
        return excerpt

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category in ['', None]:
            return self.add_error('title', '分类必须要选择')
        return category

    def clean_img(self):
        img = self.cleaned_data.get('img')
        return img

    def db_create_arctcle(self, uid):
        user = User.objects.filter(id=uid).first()
        creat_act = Article.objects.create(
            title=self.clean_title(),
            user=user,
            excerpt=self.clean_excerpt(),
            category=self.clean_category(),
            body=self.clean_body(),
            is_active=False,
        )
        try:
            file_content = ContentFile(self.request.FILES['img'].read())
            creat_act.img.save(self.request.FILES['img'].name, file_content)
        except:
            pass

    def update_arctcle(self, aid):
        artcle = Article.objects.filter(id=aid).first()
        artcle.title = self.clean_title()
        artcle.excerpt = self.clean_excerpt()
        artcle.category = self.clean_category()
        artcle.img = self.clean_img()
        artcle.body = self.clean_body()
        artcle.save()
        try:
            file_content = ContentFile(self.request.FILES['img'].read())
            artcle.img.save(self.request.FILES['img'].name, file_content)
        except:
            pass
        return artcle.user.id



