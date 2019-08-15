"""UserSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from userapp.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', RegisterView.as_view(),name="register"),
    url(r'^captcha/', include('captcha.urls')),
    #这么写是为了要取出网址中的active_code值给后台做判断
	#注：.*为正则表达式，在于去除active后面的所有字符
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='user_active' ),
    url(r'login/$',LoginView.as_view(),name='login'),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget"),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name='reset_pwd' ),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^index/$', IndexView.as_view(),name="index"),
    url(r'^logout/$', LogOutView.as_view(), name="logout"),

]
