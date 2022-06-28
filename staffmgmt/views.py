from django.shortcuts import render, redirect
from staffmgmt import models

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
    if req.method =='GET':
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

