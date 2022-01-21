#encoding=utf-8


from django import forms
from planet.models import Course, CourseArtcle
from mdeditor.fields import MDTextFormField
from django.core.files.base import ContentFile
from ceye_auth.models import User


class CourseArtcleForm(forms.ModelForm):
    part = forms.CharField(
        required=True,
        label="课程文章编号",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入课程文章编号", "class": "form-control input-sm", }
        ),
        error_messages={"required": "请输入课程文章编号, 课程文章编号不能为空"},
    )
    title = forms.CharField(
        required=True,
        label="课程文章标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入课程文章标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入课程文章标题, 课程文章标题不能为空"},
    )
    detail = MDTextFormField(required=False)

    class Meta:
        model = CourseArtcle
        fields = [
            'part', 'title', 'detail'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CourseArtcleForm, self).__init__(*args, **kw)

    def clean_part(self):
        part = self.cleaned_data.get('part')
        if part in ['', None]:
            raise forms.ValidationError('文章编号不能为空')
        return part

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('文章标题不能为空')
        return title

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        return detail

    def db_create_course(self, course_id):
        course = Course.objects.filter(id=course_id).first()
        CourseArtcle.objects.create(
            part=self.clean_part(),
            title=self.clean_title(),
            course=course,
            is_active=False,
            detail=self.clean_detail()
        )

    def update_course(self, cid):
        course_atl = CourseArtcle.objects.filter(id=cid).first()
        course_atl.part = self.clean_part()
        course_atl.title = self.clean_title()
        course_atl.detail = self.clean_detail()
        course_atl.is_active = False
        course_atl.save()




