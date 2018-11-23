# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class CITIS_users(models.Model):
    authuser = models.OneToOneField(User,on_delete=models.CASCADE)
    #username = models.CharField(u'用户名',max_length=40)
    #password = models.CharField(u'密码',max_length=40)
    type_list =(('Annoter','标注员'),('Auditor','审计员'),('Valuator','评议员'))
    utype = models.CharField(u'身份',choices=type_list,default=2,max_length=10)
    address = models.CharField(u'地址',max_length=100,null=True)
    #email = models.CharField(u'邮件',max_length=40)
    age = models.IntegerField(u'年龄',null=True)
    gender_list =(('a','女'),('b','男'))
    gender = models.CharField(u'性别',choices=gender_list,null=True,max_length=10)
    numaccount = models.CharField(u'银行卡号',null=True,max_length=17)
    phonenum = models.CharField(u'电话号码',max_length=11,null=True)
    workexper = models.TextField(blank=True)
    educationback_list = (('a','在校学生'),('b','已工作者'),('c','其他'))
    educationback = models.CharField(u'教育背景',choices=educationback_list,null=True,max_length=10)
    userlevel = models.IntegerField(u'用户等级1,2,3...',null=True)
    numuploaded = models.IntegerField(u'上传视频数量',null=True,default=0) 
    numsubmitted = models.IntegerField(u'已完成数量',default=0) 
    numacceptances = models.IntegerField(u'被接收数量',default=0)
    numrejections = models.IntegerField(u'被拒绝数量',default=0)
    blocked = models.IntegerField(u'是否被锁定',default=0)
    bonusamount = models.FloatField(u'薪酬总计',default=0) 
    verified = models.IntegerField(u'是否被认证',default=0) 
    donatedamount = models.FloatField(u'捐助数额',default=0) 

    class Meta:
        db_table = 'user_profile'
        app_label = 'userApp'


#邮箱验证的model
class EmailVerifyRecord(models.Model):
    # 验证码
    verify_code = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    # 包含注册验证和找回验证
    send_type = models.CharField(max_length=10, choices=(("register",u"注册"), ("forget",u"找回密码")))
    send_time = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = 'email_verify_records'
        app_label = 'userApp'
    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)