from __future__ import absolute_import # 绝对路径导入,因为这里的celery文件名和包名重复了，一定要写在第一行
from celery import Celery
from django.conf import settings
import os

# 设置系统的环境配置
os.environ.setdefault("DJANGO_SETTING_MODULE","UserSystem.settings")

# 实例化Celery
app = Celery("mycelery")

app.conf.timezone = "Asia/Shanghai"

# 指定celery的配置来源 用的是项目的配置文件settings.py
app.config_from_object("django.conf:settings")

# 让Celery自动去发现我们的任务
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
