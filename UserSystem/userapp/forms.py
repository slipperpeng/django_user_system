from django import forms

from captcha.fields import CaptchaField #引入验证码
class RegisterForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':'用户名不能为空'})
    password = forms.CharField(required=True,min_length=5,error_messages={'required':'密码不能为空','min_length':'密码长度不能小于5'})
    captcha = CaptchaField(error_messages={"invalid":u"验证码输入错误"}) #error_message用来显示验证码出错后的信息

class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':'用户名不能为空'})
    password = forms.CharField(required=True,error_messages={'required':'密码不能为空'})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={'required':'邮箱不能为空'})
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ModifyPwdForm(forms.Form):
    newpassword = forms.CharField(required=True,min_length=5,error_messages={'required':'密码不能为空','min_length':'密码长度不能小于5'})
    confirmpassword = forms.CharField(required=True,min_length=5,error_messages={'required':'密码不能为空','min_length':'密码长度不能小于5'})

