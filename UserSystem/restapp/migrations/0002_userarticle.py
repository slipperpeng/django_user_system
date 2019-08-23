# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-20 05:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile_article', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]