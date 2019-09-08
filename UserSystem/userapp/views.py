from django.http import HttpResponse
from django.shortcuts import render, redirect

from userapp.forms import *
from userapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password  # make_password用来将输入的密码加密成暗文
from django.views.generic.base import View
# from userapp.utils.email_send import send_register_email
from userapp.tasks import send_register_email
from django.contrib.auth.backends import ModelBackend  # 自定义的backends需要继承ModelBackend这个类
from django.db.models import Q  # Q语法用来查询并集
from rest_framework.authtoken.models import Token


####
# · create_user           创建用户
# · authenticate          登陆验证
# · login                 记录登陆状态,使用到了session
# · logout                退出用户登陆
# · is_authenticated      判断是否登陆
# · login_required装饰器   进行登陆判断

# 注册类
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form": register_form})

    def post(self, request):
        msg = ""
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username", "")
            password = request.POST.get("password", "")
            email = request.POST.get("email", "")
            user_profile = UserProfile()
            if UserProfile.objects.filter(username=user_name):
                msg = "抱歉,该用户名已被注册"
                return render(request, "register.html", {"msg": msg, "register_form": register_form})
            elif UserProfile.objects.filter(email=email):
                msg = "抱歉,该邮箱已被注册"
                return render(request, "register.html", {"msg": msg, "register_form": register_form})
            else:
                user_profile.username = user_name
                user_profile.is_active = False
                # 调用make_password来对密码进行一个加密操作
                user_profile.password = make_password(password)
                user_profile.email = email
                user_profile.save()

                # 书写send_register_email函数实现发邮件功能
                # send_register_email(email, "register")
                send_register_email.delay(email, "register")
                return render(request, 'send_success.html')
        else:
            return render(request, "register.html", {"register_form": register_form})


# 激活用户类
class ActiveUserView(View):
    def get(self, request, active_code):
        try:
            the_record = EmailVerifyRecord.objects.get(code=active_code)
            email = the_record.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()

            # 用户激活完,把之前的code给删了,防止它重复激活
            EmailVerifyRecord.objects.get(code=active_code).delete()

            # 激活完还要给用户创建个token
            Token.objects.create(user=user)
        except Exception as e:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 登录类
# 我们实现登录共有三部分验证过程
# 1.判断用户是否已经注册
# 2.判断用户注册了是否已经激活账号
# 3.判断用户的账号和密码是否正确
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 做一个表单验证判断
        login_form = LoginForm(request.POST)
        # 如果数据合法,就执行接下来的操作
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 判断该用户是否存在于用户表中(即已经注册过)
            if UserProfile.objects.filter(username=user_name) or UserProfile.objects.filter(email=user_name):
                # 引入authenticate方法对用户的用户名和密码做一个认证操作
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    if user.is_active:
                        # 判断用户是否为激活状态
                        # login函数的作用能根据用户的信息生成session id,并保存在django的session中，当退出浏览器后，将会清空这个表
                        # cookie:一种保存文件在本地的机制，可在用户访问时带上这些信息，但是不安全，所以需要session，它会从数据库中生成一段随机的session id,用户访问时带上这个id，可以实现自动登录，但是一段时间后便会过期
                        login(request, user)

                        # 登录完成后,对用户的token进行一个更新,这里调用generate_key方法来产生新的token
                        new_token = Token().generate_key()
                        Token.objects.update(user=user, key=new_token)

                        return redirect("/index/", {'user': user_name})
                    else:
                        return render(request, 'login.html', {'msg': '用户未激活!请到注册的邮箱中激活该用户！'})
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误！'})
            else:
                return render(request, 'login.html', {'msg': '该用户未注册！'})


# 找回密码类
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            emai = request.POST.get("email", "")
            if UserProfile.objects.filter(email=emai):
                # 如果该邮箱已经注册,则要判断它是否已经发过邮件了,如果表里已经存在send_type='forget'的,则要先删除，避免重复发邮件
                if EmailVerifyRecord.objects.filter(email=emai, send_type="forget"):
                    EmailVerifyRecord.objects.get(email=emai, send_type="forget").delete()
                # send_register_email(emai, "forget")
                send_register_email.delay(emai, "forget")
                return render(request, 'send_success.html')
            else:
                msg = "该邮箱还未被注册!"
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': msg})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码类
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email, 'code': active_code})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 修改密码类
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            newpassword = request.POST.get("newpassword", "")
            confirmpassword = request.POST.get("confirmpassword", "")
            email = request.POST.get("email", "")
            code = request.POST.get("code", "")
            if newpassword != confirmpassword:
                msg = "两次输入的密码不一致"
                return render(request, 'password_reset.html', {'email': email, 'msg': msg})
            if EmailVerifyRecord.objects.get(code=code):
                user = UserProfile.objects.get(email=email)
                user.password = make_password(newpassword)
                user.save()

                # 重置完,删掉原来的code,防止重复修改
                EmailVerifyRecord.objects.get(code=code).delete()

            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'modify_form': modify_form})


# 主页类
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


# 注销类
class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("/index/")


# 自定义后台认证:根据用户的邮箱等其它信息来登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 获取UserProfile数据表中对应的User,这里用到了Q查询,可以自行上网科普一下，嘿嘿~
            # 用来判断输入的指定字段是否存在于UserProfile数据表中
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 检查密码是否正确
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# ————————————分割线——————————————
# 实训扩展
# 删除消息的接口: 逻辑删除\删除的动作添加到日志中(IP地址、操作时间、行号、函数名、日志级别)
#
import logging

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


class DeleteMessageApi(View):
    # 为dispatch方法加上csrf装饰器避免403错误
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(DeleteMessageApi, self).dispatch(*args, **kwargs)

    def get(self, request):
        logger = logging.getLogger("django")
        # a = 1/0
        # print(a)
        ip_addr = request.META["REMOTE_ADDR"]
        logger.info("来自IP地址为:%s的请求" % (ip_addr))
        all_message = UserMessage.objects.filter(is_delete=False)
        msg_list = []
        for msg in all_message:
            msg_dict = {}
            msg_dict["id"] = msg.id
            msg_dict["msg"] = msg.msg
            msg_list.append(msg_dict)
        return JsonResponse(msg_list, json_dumps_params={"ensure_ascii": False}, safe=False)

    def post(self, request):
        msg_id = request.POST.get("id")
        msg = request.POST.get("msg")
        UserMessage.objects.get_or_create(id=msg_id, msg=msg)
        return HttpResponse("创建数据成功")

    def delete(self, request):
        request_body = json.loads(request.body)
        msg_id = request_body.get("id")
        UserMessage.objects.filter(id=msg_id).update(is_delete=True)
        return HttpResponse("数据删除成功")
