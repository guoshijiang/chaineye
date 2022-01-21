#encoding=utf-8


from django import forms
from planet.models import Course, CourseArtcle, CourseCommet
from mdeditor.fields import MDTextFormField
from ceye_auth.models import User


class CourseCmtForm(forms.ModelForm):
    content = MDTextFormField()

    class Meta:
        model = CourseArtcle
        fields = [
            'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CourseCmtForm, self).__init__(*args, **kw)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def db_create_course_cmt(self, course, user_id, course_atl):
        user = User.objects.filter(id=user_id).first()
        CourseCommet.objects.create(
            course=course,
            user=user,
            artcle=course_atl,
            content=self.clean_content()
        )

    def update_course_cmt(self, cid):
        course_cmt = CourseCommet.objects.filter(id=cid).first()
        course_cmt.content = self.clean_content()
        course_cmt.save()




