# Rest_FrameWork序列化器
# 1.Serializer (首先在models里面建一个UserArticle模型,然后实现create方法和update方法)
# 注意:有时候.save()方法可以重写,不一定就是拿来保存数据的,详情看文档中的API
from rest_framework import serializers
from restapp.models import *
class ArticleSerializer(serializers.Serializer):
    created = serializers.DateTimeField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()
    owner_id = serializers.IntegerField()

    def create(self, validated_data):
        return UserArticle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.content = validated_data.get("content",instance.content)
        instance.owner_id = validated_data.get("owner_id", instance.owner_id)
        instance.save()
        return instance

# # 利用serializer取数据
# all_article = UserArticle.objects.all()
# # many=True表示取多条数据,False表示取单条数据
# article = ArticleSerializer(data=all_article,many=True)
# print(article.data)
#
# # 利用serializer验证数据(和form其实差不多)
# article = ArticleSerializer(data={"title":"标题1","content":"内容1"})
# # 验证数据是否合法
# article.is_valid()
# # 输出错误信息
# article.errors
# # 如果数据无效就返回400响应
# article.is_valid(raise_exception=True)
# # 还可以只验证单个字段,详情看官方文档的API

# 2.ModelSerilalizer
# 特点:1.在普通Serializer的基础上会根据模型来自动生成一组字段
#      2.自动生成序列化器的验证器
#      3.默认简单地实现了.create()方法和.update()方法
from rest_framework.serializers import ModelSerializer
class ArticleModelSerializer(ModelSerializer):
    class Meta:
        model = UserArticle
        # 设置要序列的字段
        # fields = "__all__" 则表明使用模型中的所有字段
        # 可以将exclude属性设置成一个从序列化器中排除的字段列表: exclude = ("created")
        # fields = ("id","created","content","owner")
        fields = "__all__"
        # 深度控制,1为取1层，取和它关联表的数据
        depth = 1

# 经过上面的操作,是把全部数据取出来了,那如果我想自定制呢？比如我只想取出和它关联的用户名
class CustomArticleModelSerializer(ModelSerializer):
    owner_username = serializers.CharField(source='owner.username')
    class Meta:
        model = UserArticle
        fields = ("id","created","content","owner","owner_username")

# 3.HyperlinkedModelSerializer
#HyperlinkedModelSerializer类类似于ModelSerializer类，不同之处在于它使用超链接来表示关联关系而不是主键。
# 说得通俗点,就是可以在页面上生成url,点进去就是对应的数据
from rest_framework.serializers import HyperlinkedModelSerializer
class ArticleHyperlinkModelSerializer(HyperlinkedModelSerializer):
    # 这里的view_name与url中的name对应，lookup_field,默认是pk,而我们数据库中实际存储的字段名为owner_id
    owner = serializers.HyperlinkedIdentityField(view_name="article_owner_detail",lookup_field="owner_id",lookup_url_kwarg="xxx")
    class Meta:
        model = UserArticle
        fields = ("id","created","content","owner")

class ArticleOwnerSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

# 小笔记部分
# 对于普通的对象,many=False 交给Serializer  many=True,则交给ListSerializer

# 接下来是分页器,先去settings里面配置page_size
