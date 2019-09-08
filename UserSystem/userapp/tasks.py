from celery import task
import time

# 书写函数时要加上task装饰器

from userapp.models import EmailVerifyRecord
from random import Random
from django.core.mail import  send_mail
from UserSystem.settings import  EMAIL_FROM


#这个函数用来生成一段随机的验证码字符串,这里可以自己扩展需要的字符串类型

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

@task
# 引用Django内置的send_mail模块进行发送
def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = 'Django用户系统激活链接'
        email_body = '''
                    您好：
                    感谢您注册Django用户系统账号,请点击以下链接进行邮箱验证！若无法点击，请将链接复制到浏览器打开。此链接将在24小时后失效。
                    请点击下面的链接激活您的账号:http://127.0.0.1:8000/active/{0}'''.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = 'Django用户系统找回密码链接'
        email_body = '''
                    尊敬的Django用户,您好：
                    虽然忘了密码这件事情很羞耻哈哈哈，但还是请你点击以下链接进行找回密码操作！若无法点击，请将链接复制到浏览器打开。此链接将在24小时后失效。
                    请点击下面的链接找回你的密码:http://127.0.0.1:8000/reset/{0}'''.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass