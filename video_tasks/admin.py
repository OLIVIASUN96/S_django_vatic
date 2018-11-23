# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from video_tasks.models import Video,Job,Segment
from userApp.models import CITIS_users



class SegmentInline(admin.StackedInline):
    model = Job
    extra = 0

class SegmentAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    inlines = [SegmentInline]
    list_display=('video_id','start','stop','id')
    #list_filter = ('id',)

class VideoInline(admin.StackedInline):
    model = Segment
    extra = 0

class VideoAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    inlines = [VideoInline]
    list_display=('slug','totalframes','location')
    #list_filter = ('id',)

class JobAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display=('id','istraining','segment_id')
    #list_filter = ('id',)

class ProfileInline(admin.StackedInline):
    model = CITIS_users
    max_num = 1

class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline,]


#admin.site.register(Task,TaskAdmin) #向管理网站添加Task类模型
admin.site.register(Segment,SegmentAdmin)
admin.site.register(Video,VideoAdmin)
admin.site.register(Job,JobAdmin)
#admin.site.unregister(User)
#admin.site.register(User,UserProfileAdmin)
# admin.site.register(Entry)
#admin.site.register(Video,VideoAdmin)
