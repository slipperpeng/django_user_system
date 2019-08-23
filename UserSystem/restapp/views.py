from restapp.models import *
from django.views.generic import View
from django.shortcuts import render,redirect,HttpResponse


from rest_framework.views import APIView
from restapp.serializers import *
from rest_framework.response import Response
from rest_framework import status
from restapp.three_processes import CustomThrottle
from rest_framework.pagination import PageNumberPagination

# 自定义一个分页器类,实现高度自定制(还可以自定制加密的分页器类,详情看文档咯)
class CustomPageNumberPagination(PageNumberPagination):
    # 一页默认显示2个
    page_size = 2
    # 在url后缀page_size = 3 表示一页显示3条
    page_size_query_param = "page_size"
    # 设置一页最多显示5条
    max_page_size = 5
    # 在url后缀page=1 表示显示第一页的内容
    page_query_param = "page"

# 书写一个ArticlePostDetail类
class ArticlePostDetail(APIView):
    # 让这个接口一分钟内只能被访问3次,配置在settings.py中
    throttle_classes = (CustomThrottle,)
    def get(self,request,*args,**kwargs):
        # 获取所有对象
        article_detail = UserArticle.objects.all()
        # # 加上分页器功能
        pg = CustomPageNumberPagination()

        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=article_detail,request=request,view=self)

        # article_serializer = ArticleModelSerializer(instance=article_detail,many=True)
        # article_serializer = CustomArticleModelSerializer(instance=article_detail, many=True)
        article_serializer = ArticleHyperlinkModelSerializer(pager_roles, many=True,context={'request': request})
        return Response(article_serializer.data)

    def post(self,request):
        print(request.data)
        # article_serializer = ArticleSerializer(data=request.data)
        article_serializer = ArticleModelSerializer(data=request.data)
        if article_serializer.is_valid():
            print("数据合法")
            article_serializer.save()
            # 这个Response来自Rest_framework中,传入HTTP状态作为响应
            return Response(article_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(article_serializer.errors)
            content = {'please move along': 'nothing to see here'}
            return Response(content,status=status.HTTP_404_NOT_FOUND)

# HyperlinkedModelSerializer的类
class ArticleOwnerDetail(APIView):
    def get(self,request,*args,**kwargs):
        owner_id = kwargs.get("xxx")
        print(owner_id)
        article_owner_detail = UserProfile.objects.filter(id=owner_id).first()
        article_owner_detail_serializer = ArticleOwnerSerializer(instance=article_owner_detail, many=False,context={'request': request})
        return Response(article_owner_detail_serializer.data)

# ————————分割线——————————
# 使用GenericAPIView重写ArticlePostDetail类（GET请求）
# GenericAPIView是继承于APIView的一个子类,代码看起来更简洁(但是我觉得APIView的逻辑比较清晰点)
from rest_framework.generics import GenericAPIView
class OverRideArticlePostDetail(GenericAPIView):
    # 让这个接口一分钟内只能被访问3次,配置在settings.py中
    throttle_classes = (CustomThrottle,)
    queryset = UserArticle.objects.all()
    serializer_class = ArticleHyperlinkModelSerializer
    pagination_class = CustomPageNumberPagination
    def get(self,request,*args,**kwargs):
        # 获取所有对象
        article_detail = self.get_queryset()

        # 加上分页器功能并在数据库中获取分页的数据
        pager_roles = self.paginate_queryset(article_detail)

        # 使用对应的序列化器
        article_serializer = self.get_serializer(pager_roles, many=True,context={'request': request})
        return Response(article_serializer.data)


# 使用GenericViewSet重写ArticlePostDetail类（GET请求）
# GenericViewSet继承了两个爸爸(ViewSetMixin,GenericAPIView)
# ViewSetMixin对as_view方法进行了重写,所以url中的as_view()里面要加参数
# 其实和GenericAPIView没区别,就url加参数,方法命名变一变
from rest_framework.viewsets import GenericViewSet
class AgainOverRideArticlePostDetail(GenericViewSet):
    # 让这个接口一分钟内只能被访问3次,配置在settings.py中
    throttle_classes = (CustomThrottle,)
    queryset = UserArticle.objects.all()
    serializer_class = ArticleHyperlinkModelSerializer
    pagination_class = CustomPageNumberPagination
    def list(self,request,*args,**kwargs):
        # 获取所有对象
        article_detail = self.get_queryset()

        # 加上分页器功能并在数据库中获取分页的数据
        pager_roles = self.paginate_queryset(article_detail)

        # 使用对应的序列化器
        article_serializer = self.get_serializer(pager_roles, many=True,context={'request': request})
        return Response(article_serializer.data)


# 使用ModelViewSet重写ArticlePostDetail类（GET请求）
# ModelViewSet...是最终的Boss,里面继承了多个实现类,如list(get请求),create(请求)等
# 让你解放双手,从此不用多写下面的方法
from rest_framework.viewsets import ModelViewSet
class LastOverRideArticlePostDetail(ModelViewSet):
    throttle_classes = (CustomThrottle,)
    queryset = UserArticle.objects.all()
    serializer_class = ArticleHyperlinkModelSerializer
    pagination_class = CustomPageNumberPagination


# 渲染器和页面解析器,可以自行去了解
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
