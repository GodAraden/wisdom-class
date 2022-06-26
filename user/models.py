from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type = models.IntegerField(verbose_name='用户类型',null=True)
    sex = models.CharField(max_length=10, default='',verbose_name='性别')
    name = models.CharField(max_length=20, default='',verbose_name='姓名')
    birday = models.DateField(verbose_name='生日', null=True, blank=True)
    user_email = models.EmailField(verbose_name="user_email", default='')
    number = models.CharField(max_length=20,default='',verbose_name='学号')
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
    def set_user_type(self,user_type):
        self.user_type = user_type
    def set_sex(self,sex):
        self.sex = sex
    def set_birthday(self,birthday):
        self.birday = birthday
    def set_name(self,n):
        self.name = n
    def set_email(self,email):
        self.user_email = email
    def set_number(self,number):
        self.number = number

class TeacherPhone(models.Model):
    phone = models.CharField('phone',max_length=11)
    used = models.BooleanField('used',default=False)
    class Meta:
        verbose_name = '教职工手机号' # 表中数据为单数的时候admin后台中展示的名称
        verbose_name_plural = verbose_name # 表中数据为复数的时候admin后台中展示的名称