from django.shortcuts import render, redirect
from staffmgmt import models
from django import forms
from django.utils.safestring import mark_safe

from staffmgmt.utils.pagination import Pagination


# Create your views here.


def depart_list(req):
    # 从数据库获取数据
    depart_list = models.Department.objects.all()
    pagination_obj = Pagination(req, depart_list, page_size=3)
    render_dict = {
        'depart_list': pagination_obj.page_queryset,
        'http_string': pagination_obj.make_html(),
    }
    return render(req, 'depart_list.html', render_dict)


def depart_add(req):
    if req.method == 'GET':
        return render(req, 'depart_add.html')
    title = req.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')


def depart_delete(req):
    nid = req.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit(req, nid):
    if req.method == 'GET':
        row = models.Department.objects.filter(id=nid).first()
        return render(req, 'depart_edit.html', {'row': row})
    title = req.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


def user_list(req):
    query_set = models.UserInfo.objects.all()
    pagination_obj = Pagination(req, query_set, page_size=2)
    render_dict = {
        'query_set': pagination_obj.page_queryset,
        'http_string': pagination_obj.make_html(),
    }
    return render(req, 'user_list.html', render_dict)


##################   ModelForm方式添加用户   ##########################




class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'salary', 'gender', 'depart', 'create_time']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def user_modelform_add(req):
    if req.method == 'GET':
        form = UserModelForm()
        return render(req, 'user_modelform_add.html', {'form': form})
    # 用户post提交数据的话
    form = UserModelForm(data=req.POST)
    # 校验用户提交的数据是否无误
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    # 如果用户提交数据有误，再页面上展示错误原因 html里以 {{ field.error.0 }} 去取第一个错误信息
    return render(req, 'user_modelform_add.html', {'form': form})


def user_edit(req, nid):
    if req.method == 'GET':
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(req, 'user_edit.html', {'form': form})
    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=req.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(req, 'user_edit.html', {'form': form})


def user_del(req, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(req):
    # 添加搜索靓号功能
    serch_dict = {}
    serch_value = req.GET.get('ser_data', '')
    if serch_value:
        serch_dict['mobile__contains'] = serch_value
    queryset = models.PrettyNum.objects.filter(**serch_dict).order_by('-level')


    # 创建一个分页类的实例
    pagination_obj = Pagination(req, queryset)
    render_dict = {
        'serch_value': serch_value,
        'query_set': pagination_obj.page_queryset,
        'page_str': pagination_obj.make_html(),
    }
    return render(req, 'prettynum_list.html', render_dict)


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class PrettyNumForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = '__all__'
    # 验证方法1:
    mobile = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '请输入正确的手机号格式！')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
    # 验证方法2:
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exist = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exist:
            raise ValidationError('手机号已存在！')
        return txt_mobile


def pretty_add(req):
    if req.method == 'GET':
        form = PrettyNumForm()
        return render(req, 'pretty_add.html', {'form': form})
    form = PrettyNumForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(req, 'pretty_add.html', {'form': form})


# 为“靓号编辑”定义的ModelForm类和view函数：
class PrettyEditModelForm(forms.ModelForm):
    # 数据校验1
    mobile = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '输入的手机号格式不正确！！！')])
    # mobile = forms.CharField(disabled=True, label='手机号') 编辑的时候显示手机号但是不可以进行编辑，使用disable=True参数


    class Meta:
        model = models.PrettyNum
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
    # 通过钩子函数进行数据校验：
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        current_id = self.instance.pk
        exist = models.PrettyNum.objects.exclude(id=current_id).filter(mobile=txt_mobile).exists()
        if exist:
            raise ValidationError('手机号已存在！请输入新的号码~')
        return txt_mobile



def pretty_edit(req, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if req.method == 'GET':
        form = PrettyEditModelForm(instance=row_obj)
        return render(req, 'pretty_edit.html', {'form': form})
    form = PrettyEditModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(req, 'pretty_edit.html', {'form': form})

def pretty_del(req, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')



