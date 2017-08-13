# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from video_tasks.models import Task,Entry

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0
    
class TaskAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    inlines = [EntryInline]
    list_display=('text','owner','date_added')
    list_filter = ('date_added',)

   

admin.site.register(Task,TaskAdmin) #向管理网站添加Task类模型
# admin.site.register(Entry)
