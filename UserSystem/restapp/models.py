from django.db import models
from userapp.models import *

class PermissionLimit(models.Model):
    black_list = models.CharField(max_length=20, blank=True, null=True)


class UserArticle(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True,default='')
    content = models.CharField(max_length=400,blank=True,default='')
    owner = models.ForeignKey(UserProfile, related_name='userprofile_article', on_delete=models.CASCADE)

