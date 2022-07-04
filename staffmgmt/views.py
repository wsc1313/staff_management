from django.shortcuts import render, redirect
from staffmgmt import models
from django.utils.safestring import mark_safe


# Create your views here.


def depart_list(req):
    # 从数据库获取数据
    depart_list = models.Department.objects.all()
    return render(req, 'depart_list.html', {'depart_list': depart_list})


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
    return render(req, 'user_list.html', {'query_set': query_set})


##################   ModelForm方式添加用户   ##########################

from django import forms


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
    # for i in range(0, 300):
    #     models.PrettyNum.objects.create(mobile='18888888888', price=10, level=1, status=2)
    page_num = int(req.GET.get('page', 1))
    page_size = 10
    start = (page_num - 1) * page_size
    end = page_num * page_size
    query_set = models.PrettyNum.objects.all().order_by('-level')[start:end]
    total_count = models.PrettyNum.objects.all().count()
    total_page_cout, div = divmod(total_count, page_size)
    if div:
        total_page_cout += 1
    # 计算出当前页的前5页 和 后5页
    plus = 5
    if total_page_cout <= plus * 2 +1:
        start_page = 1
        end_page = total_page_cout
    else:
        if page_num <= plus:
            start_page = 1
            end_page = plus * 2 + 1
        else:
            if page_num + plus > total_page_cout:
                end_page = total_page_cout
                start_page = total_page_cout - plus * 2
            else:
                start_page = page_num - plus
                end_page = page_num + plus

    page_str_list = []
    # 尾页
    page_str_list.append('<li><a href="?page=1">首页</a></li>')
    # 上一页
    if page_num > 1:
        prev = page_num - 1
        tpl = f'<li><a href="?page={prev}">上一页</a></li>'
    else:
        tpl = '<li><a href="?page=1">上一页</a></li>'
    page_str_list.append(tpl)

    for i in range(start_page, end_page + 1):
        if i == page_num:
            tpl = f'<li class="active"><a href="?page={i}">{i}</a></li>'
        else:
            tpl = f'<li><a href="?page={i}">{i}</a></li>'
        page_str_list.append(tpl)
    # 下一页
    if page_num < total_page_cout:
        prev = page_num + 1
        tpl = f'<li><a href="?page={prev}">下一页</a></li>'
    else:
        tpl = f'<li><a href="?page={total_page_cout}">下一页</a></li>'
    page_str_list.append(tpl)

    # 尾页
    page_str_list.append(f'<li><a href="?page={total_page_cout}">尾页</a></li>')

    # 指定页面搜索
    serch_string = """
        <li>
            <form method="get" style='float:left;margin-left:-1px'>
                <input type="text" name='page' style='position:relative;float:left;display:inline-block;width:80px;border-radius:0;' 
                class="form-control" placeholder="页码">
                <button class="btn btn-default" type="submit">Go!</button>
            </form>
        </li>
        """
    page_str_list.append(serch_string)

    page_str = mark_safe(''.join(page_str_list))


    return render(req, 'prettynum_list.html', {'query_set': query_set, 'page_str': page_str})


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class PrettyNumForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = '__all__'
    # 验证方法1：
    mobile = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '请输入正确的手机号格式！')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

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
    # 数据校验
    mobile = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '输入的手机号格式不正确！！！')])

    class Meta:
        model = models.PrettyNum
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

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



