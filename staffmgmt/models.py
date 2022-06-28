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
