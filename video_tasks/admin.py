# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from video_tasks.models import Task,Entry


admin.site.register(Task) #向管理网站添加Task类模型
admin.site.register(Entry)
