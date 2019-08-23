import datetime
import pytz
# 我们来说个Session认证和token认证的区别
# session: 不同于cookie，却需要用到cookie,将session_id存于数据库或缓存中,实现用户维持会话的操作
# PS： 即便你禁用浏览器上的cookie，它依然能将session_id附在url后面进行传递

# token：Token 是在服务端产生的，如果前端使用用户名/密码向服务端请求认证，
# 服务端认证成功，那么在服务端会返回 Token 给前端。
# 前端可以在每次请求的时候带上 Token 证明自己的合法地位。

# session遇到移动端就萎了,而token则不会,那么我们就用token来搞吧~
#————————————分割线———————————————
# 首先,我们先自定义个用户流程类,当然了,我们使用django自带的TokenAuthentication可以伐？可以！
# 但是,自带的token认证它老是要去数据库中取东西，这样对性能其实也有损耗,我们只需要重写它里面的authenticate_credentials方法,增加缓存机制即可
# 操作如下:
# 1.继承默认的TokenAuthentication
# 2.重写authenticate_credentials方法,加入缓存机制,并对token的过期时间做一个判断
# 注意事项:
# 1.你要继承TokenAuthentication，就要用它默认的token表,自己定义的话,也可以,但是需要返回两个属性(token,user)
# 2.前端发来的请求头token的格式:  Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
from rest_framework.authentication import TokenAuthentication
from rest_framework import  exceptions #rest_framework内置的异常模块
from django.utils.translation import ugettext_lazy as _ #惰性翻译,django的一个国际化操作
from django.core.cache import cache


class CustomAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        token_cache =  'token_' + key
        #cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None)
        is_cache = cache.get(token_cache)
        if is_cache:
            print(is_cache.user,token_cache)
            return (is_cache.user,is_cache)
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # 设置token的过期时间为14天
        utc_now = datetime.datetime.utcnow()
        if (utc_now.replace(tzinfo=pytz.timezone("UTC")) - token.created.replace(
                tzinfo=pytz.timezone("UTC"))).days > 14:
            raise exceptions.AuthenticationFailed(_('Authentication information expired'))

        # 设缓存的时间为2小时
        cache.set(token_cache, token, 2 * 60 * 60)
        return (token.user, token)

# 然后我对用户激活类和用户登录类分别做了一点代码的增加
# 增加内容如下:
    # 1.ActiveUserView 增加在用户激活完账户后,往token表中创建一条记录,为该用户创建一个token
    # 2.LoginView 增加在用户登录时,对token进行更新

# 接下来写第二步: 用户权限(permissions)
# 操作如下:
# 1.设置IP地址黑名单,如果来访的用户的IP地址在黑名单上,则禁止访问.
# 2.如果用户的身份是vip用户,我们才给他访问,否则不给访问
# 首先对默认的UserProfile表添加一个字段black_list用来记录用户的IP地址
# 然后再添加一个用户的类型字段,用来判断该用户属于什么类型的用户(普通vip,高级vip....)
from rest_framework.permissions import BasePermission
from restapp.models import *
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        ip_addr = request.META["REMOTE_ADDR"]
        print("来访用户的IP地址为:",ip_addr)
        # 不要问我为啥这么写判断,django官方说这样操作最快...
        if PermissionLimit.objects.filter(black_list=ip_addr).exists():
            return False
        # 如果用户未登录,不给他们看,hhhh
        if not request.user.is_authenticated():
            return False
        # 如果用户登录了,则判断他们的用户类型,vip用户才能看
        user = UserProfile.objects.get(username=request.user)
        if not user.user_type == "vip用户":
            return False
        return True


# 接下来写最后一步: 用户限流
# 这个接口不允许用户频繁地进行访问,可以设置成我想要的访问速率
from rest_framework.throttling import SimpleRateThrottle
# SimpleRateThrottle的源码流程:
# 1.找rate属性,如果rate为None,则表明不想设置频率限制,return True
# 2.如果rate不为None,就找scope属性,找不到,抛出异常.找到了,根据scope属性的值，去用户自定义的settings中找出对应的请求次数/周期
# 3.根据拿到的请求次数/周期(如:3/m),进行分割,分别取出次数和周期,赋值给num_requests和duration
# 4.执行allow_request方法,会跟着get_cache_key()方法,这个方法必须由用户来进行重写,必须的！这里对get_cache_key()返回了一个用户的IP
# 5.将用户的IP作为key,一个ip对应一个history,刚开始会从缓存中读取,然后做一些判断,最后没问题就调用throttle_success方法
# 6.throttle_success方法则会将当前时间加入到history中,并对key设置缓存,懂我意思吧~
class CustomThrottle(SimpleRateThrottle):
    scope = "xxx"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
