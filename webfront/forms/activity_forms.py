#encoding=utf-8


from django import forms
from activity.models import Area, Category, Activity
from DjangoUeditor.forms import UEditorField
from django.core.files.base import ContentFile
from ceye_auth.models import User


class ActivityForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="活动标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动标题"}
        ),
    )
    category = forms.ModelChoiceField(
        empty_label="请选择活动类别",
        queryset = Category.objects.filter(type="Activity", is_active=True)
    )
    position = forms.CharField(
        required=True,
        label="活动详细地点",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动详细地点", "class": "form-control"}
        ),
        error_messages={"required": "请输入活动详细地点, 活动详细地点不能为空"},
    )
    area = forms.ModelChoiceField(
        empty_label="活动地区",
        queryset=Area.objects.filter(is_active=True)
    )
    act_time = forms.CharField(
        required=True,
        label="活动时间",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动时间", "class": "form-control"}
        ),
        error_messages={"required": "请输入活动时间, 活动时间不能为空"},
    )
    excerpt = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'style': 'height:200px; width:800px',
                'placeholder': '请输入活动简介'

            }
        )
    )
    company = forms.CharField(
        required=True,
        label="活动举办单位",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动举办单位", "class": "form-control"}
        ),
        error_messages={"required": "请输入活动举办单位, 活动举办单位不能为空"},
    )
    author = forms.CharField(
        required=True,
        label="活动发起人",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动发起人", "class": "form-control"}
        ),
        error_messages={"required": "请输入活动发起人, 活动发起人不能为空"},
    )
    actfee = forms.CharField(
        required=True,
        label="活动费用",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动费用", "class": "form-control"}
        ),
        error_messages={"required": "请输入活动费用, 活动费用不能为空"},
    )
    person = forms.CharField(
        required=True,
        label="活动人数上限",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入活动人数上限", "class": "form-control"}
        ),
        error_messages={"required": "请输入活动人数上限, 活动人数上限不能为空"},
    )
    img = forms.ImageField(
        required=True,
        error_messages={"invalid": "请上传图片, 图片不能为空"},
    )
    body = UEditorField(
        label='活动内容',
        width=960, height=900,
        toolbars="full",
        imagePath="upimg/",
        filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}
    )
    status = forms.CharField(
        label="活动状态",
        initial=2,
        widget=forms.Select(
            choices=(('UnStart', '未开始'), ('Starting', '报名中'),('Finished', '已完成'),)
        ),
    )

    class Meta:
        model = Activity
        fields = [
            'title', 'category', 'position', 'area',
            'act_time', 'excerpt', 'company', 'author',
            'actfee', 'person', 'img', 'body', "status"
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(ActivityForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('活动标题不能为空')
        return title

    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category

    def clean_position(self):
        position = self.cleaned_data.get('position')
        if position in ['', None]:
            raise forms.ValidationError('活动详细地点不能为空')
        return position

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area in ['', None]:
            raise forms.ValidationError('活动地区不能为空')
        return area

    def clean_act_time(self):
        act_time = self.cleaned_data.get('act_time')
        if act_time in ['', None]:
            raise forms.ValidationError('活动时间不能为空')
        return act_time

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt in ['', None]:
            raise forms.ValidationError('文章摘要不能为空')
        return excerpt

    def clean_company(self):
        company = self.cleaned_data.get('company')
        if company in ['', None]:
            raise forms.ValidationError('活动举办公司不能为空')
        return company

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if author in ['', None]:
            raise forms.ValidationError('活动发起人不能为空')
        return author

    def clean_actfee(self):
        actfee = self.cleaned_data.get('actfee')
        if actfee in ['', None]:
            raise forms.ValidationError('活动费用不能为空，如果不收费，请填写免费')
        return actfee

    def clean_person(self):
        person = self.cleaned_data.get('person')
        if person in ['', None]:
            raise forms.ValidationError('活动人数上限不能为空')
        return person

    def clean_img(self):
        img = self.cleaned_data.get('img')
        return img

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body in ['', None]:
            raise forms.ValidationError('文章内容不能为空')
        return body

    def clean_status(self):
        status = self.cleaned_data.get('status')
        return status

    def create_activity(self, user_id):
        user = User.objects.filter(id=user_id).first()
        create_act = Activity.objects.create(
            title=self.clean_title(),
            category=self.clean_category(),
            position=self.clean_position(),
            area=self.clean_area(),
            user=user,
            act_time=self.clean_act_time(),
            excerpt=self.clean_excerpt(),
            company=self.clean_company(),
            author=self.clean_author(),
            actfee=self.clean_actfee(),
            person=self.clean_person(),
            body=self.clean_body(),
            status=self.clean_status(),
        )
        try:
            file_content = ContentFile(self.request.FILES['img'].read())
            create_act.img.save(self.request.FILES['img'].name, file_content)
        except:
            pass

    def update_activity(self, act_id):
        act = Activity.objects.filter(id=act_id).first()
        act.title = self.clean_title()
        act.category = self.clean_category()
        act.position = self.clean_position()
        act.area = self.clean_area()
        act.act_time = self.clean_act_time()
        act.excerpt = self.clean_excerpt()
        act.company = self.clean_company()
        act.author = self.clean_author()
        act.actfee = self.clean_actfee()
        act.person = self.clean_person()
        act.body = self.clean_body()
        act.status = self.clean_status()
        try:
            file_content = ContentFile(self.request.FILES['img'].read())
            act.img.save(self.request.FILES['img'].name, file_content)
        except:
            pass





