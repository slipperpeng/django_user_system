from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
#这里做个演示,只扩展两个字段
# blank=True 表示该数据可不填，blank 是针对表单的
# null=True 表示数据允许为空, null 是针对数据库的
# blank只是在填写表单的时候可以为空，而在数据库上存储的是一个空字符串；null是在数据库上表现NULL，而不是一个空字符串；
# blank主要是用在CharField, TextField,这两个字符型字段可以用空字符穿来储存空值。
# null主要是用在IntegerField，DateField, DateTimeField,这几个字段不接受空字符串，所以在使用时，必须将blank和null同时赋值为True。
vip_choices = ((0,'普通用户'),(1,'vip用户'),(2,'svip用户'))
class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    # ——————Rest_framework扩展的字段(user_type)——————————
    user_type = models.IntegerField(choices=vip_choices,default=0)
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.username

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.CharField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name=u"验证码类型",choices=(("register",u"注册"),("forget",u"找回密码")),max_length=10)
    send_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name