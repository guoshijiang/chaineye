#encoding=utf-8


from django import forms
from planet.models import Course, CourseCat
from mdeditor.fields import MDTextFormField
from django.core.files.base import ContentFile
from ceye_auth.models import User
from common.helpers import dec


class CourseForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="课程标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入课程标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入课程标题, 课程标题不能为空"},
    )
    logo = forms.ImageField(
        required=True,
        error_messages={"invalid": "请上传图片, 图片不能为空"},
    )
    excerpt = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'style': 'height:200px; width:100%;outline: none;padding: 15px;box-sizing: border-box;',
                'placeholder': '请输入课程摘要，不少于 100 字'
            }
        )
    )
    category = forms.ModelChoiceField(
        empty_label="请选择课程类别",
        queryset=CourseCat.objects.filter(is_active=True)
    )
    detail = MDTextFormField()
    price = forms.CharField(
        required=True,
        label="课程价格",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入课程价格", "class": "form-control"}
        ),
        error_messages={"required": "请输入课程价格, 课程价格不能为空"},
    )

    class Meta:
        model = Course
        fields = [
            'title', 'logo', 'excerpt', 'category', 'detail', 'price'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CourseForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('课程标题不能为空')
        return title

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        return logo

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt in ['', None]:
            raise forms.ValidationError('课程简介不能为空')
        return excerpt

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category in ['', None]:
            return self.add_error('title', '课程分类必须要选择')
        return category

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        return detail

    def clean_price(self):
        price = dec(self.cleaned_data.get('price'))
        if price < 0:
            raise forms.ValidationError('课程价格无效，情输入大于等于0的数字')
        return price

    def db_create_course(self, uid):
        user = User.objects.filter(id=uid).first()
        creat_cource = Course.objects.create(
            title=self.clean_title(),
            excerpt=self.clean_excerpt(),
            category=self.clean_category(),
            price=self.clean_price(),
            user=user,
            detail=self.clean_detail()
        )
        try:
            file_content = ContentFile(self.request.FILES['logo'].read())
            creat_cource.logo.save(self.request.FILES['logo'].name, file_content)
        except:
            pass

    def update_course(self, cid):
        course = Course.objects.filter(id=cid).first()
        course.title = self.clean_title()
        course.excerpt = self.clean_excerpt()
        course.category = self.clean_category()
        course.price = self.clean_price()
        course.detail = self.clean_detail()
        course.save()
        try:
            file_content = ContentFile(self.request.FILES['logo'].read())
            course.logo.save(self.request.FILES['logo'].name, file_content)
        except:
            pass
        return course.user.id

