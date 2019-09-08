"""UserSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.conf.urls import url,include
from django.contrib import admin
from userapp.views import *

# rest_framework
from restapp.views import *
from rest_framework import routers

# 这两行是为了最后的视图而添加的
router = routers.DefaultRouter()
router.register(r"xxx",LastOverRideArticlePostDetail)

from django.views import static ##新增
from django.conf import settings ##新增

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^register/$", RegisterView.as_view(),name="register"),
    url(r"^captcha/", include("captcha.urls")),
    # 这么写是为了要取出网址中的active_code值给后台做判断
	# 注：.*为正则表达式，在于去除active后面的所有字符
    url(r"^active/(?P<active_code>.*)/$",ActiveUserView.as_view(),name="user_active" ),
    url(r"login/$",LoginView.as_view(),name="login"),
    url(r"^forget/$", ForgetPwdView.as_view(), name="forget"),
    url(r"^reset/(?P<active_code>.*)/$",ResetView.as_view(),name="reset_pwd" ),
    url(r"^modify_pwd/$", ModifyPwdView.as_view(), name="modify_pwd"),
    url(r"^index/$", IndexView.as_view(),name="index"),
    url(r"^logout/$", LogOutView.as_view(), name="logout"),

    # rest_framework
    url(r"^article_post_detail/$",ArticlePostDetail.as_view(),name="article_post_detail"),
    # HyperlinkedModelSerializer的url
    url(r"^article_post_detail/owner/(?P<xxx>\d+)/$",ArticleOwnerDetail.as_view(),name="article_owner_detail"),
    # GenericAPIView
    url(r"^over_ride_article_post_detail/$",OverRideArticlePostDetail.as_view(),name="over_ride_article_post_detail"),
    # GenericViewSet (这里参数的意思是,get方法就用list来命名）
    url(r"^again_over_ride_article_post_detail/$",AgainOverRideArticlePostDetail.as_view({'get':'list'}),name="again_over_ride_article_post_detail"),
    # ModelViewSet ,终极视图类(几行代码实现增删改查)
    # url(r"^last_over_ride_article_post_detail/$",LastOverRideArticlePostDetail.as_view({'get':'list'}),name="last_over_ride_article_post_detail"),
    # url(r"^last_over_ride_article_post_detail/(?P<pk>\d+)/$", LastOverRideArticlePostDetail.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),name="last_over_ride_article_post_detail"),
    # url(r'^last_over_ride_article_post_detail\.(?P<format>[a-z0-9]+)$', LastOverRideArticlePostDetail.as_view()),
    # url(r'^last_over_ride_article_post_detail/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)$', last_over_ride_article_post_detail.as_view()

    # 这一行等于上面4句
    url(r'^', include(router.urls)),

    # 实训扩展
    # DeleteMessageApi
    url(r'^deletemessageapi/$',DeleteMessageApi.as_view()),
]
