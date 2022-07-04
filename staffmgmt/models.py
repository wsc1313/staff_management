from django.db import models

# Create your models here.


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=32)
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    salary = models.DecimalField(verbose_name='薪资', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', blank=True, null=True, on_delete=models.SET_NULL)
    gender_choice = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)

class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choice = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
    )
    status_choice = (
        (1, '已使用'),
        (2, '未使用'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choice, default=1)
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=2)


