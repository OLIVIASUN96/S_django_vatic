# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from learning_logs.models import Topic,Entry


admin.site.register(Topic) #向管理网站添加Topic类模型
admin.site.register(Entry)
