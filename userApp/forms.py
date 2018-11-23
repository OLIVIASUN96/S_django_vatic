#!/usr/bin/env python
# coding=utf-8
from django.contrib.auth.models import User
from django import forms
from userApp.models import CITIS_users
from learning.core.models import *


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=u'用户名',
        help_text=u'用户名可用于登录，不能包含空格和@字符。',
        max_length=40,
        min_length=3,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

    email = forms.EmailField(
        label=u'邮箱',
        help_text=u'邮箱可用于登录，最重要的是需要邮箱来找回密码，所以请输入您的可用邮箱。',
        max_length=40,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

    phonenum = forms.CharField(
        label=u'电话',
        help_text=u'电话作为联系方式之一，发布任务和通知奖励情况。',
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
    banknum = forms.CharField(
        label=u'银行卡号',
        help_text=u'用于发放薪酬的银行卡号。',
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
    
    age = forms.CharField(
        label=u'年龄',
        help_text=u'请输入年龄。',
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
    sex = forms.ChoiceField(
        label = u'性别',
        choices = (('a','男'),('b','女')),
        widget = forms.RadioSelect,
        help_text = u'请选择您的性别',
    )
    #下拉框
    edubackground = forms.ChoiceField(
        label=u'教育背景',
        choices=[('a','在校学生'),('b','已工作者'),('c','其他')],
        help_text=u'请选择您的教育背景。',
        #initial='',       
        )
    #下拉框
    usertype = forms.ChoiceField(
        label=u'用户类型',
        choices=[('Annoter','标注员'),('Auditor','审计员'),('Valuator','评议员')],
        help_text=u'请选择注册用户类型。',
        #initial='',        
        )
    password = forms.CharField(
        label=u'密码',
        help_text=u'密码只有长度要求，长度为 6 ~ 18 。',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )

    confirm_password = forms.CharField(
        label=u'确认密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username or '@' in username:
            raise forms.ValidationError(u'昵称中不能包含空格和@字符')
        res = User.objects.filter(username=username)
        if len(res) != 0:
            raise forms.ValidationError(u'此昵称已经注册，请重新输入')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        res =User.objects.filter(email=email)
        if '@' not in email:
            raise forms.ValidationError(u'请正确输入邮箱')
        if len(res) != 0:
            raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
        return email

    #感觉电话可以被重复注册啊..... 先暂时注释掉
    #def clean_phonenum(self):
        #phonenum = self.cleaned_data['phonenum']
        #res = CITIS_users.objects.filter(phonenum=phonenum)
        #if len(res) != 0:
            #raise forms.ValidationError(u'此phone已经注册，请重新输入')
        #return phonenum

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(u'两次密码输入不一致，请重新输入')

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        age = self.cleaned_data['age']
        phoneNum = self.cleaned_data['phonenum']
        password = self.cleaned_data['password']
        usertype = self.cleaned_data['usertype']
        sex = self.cleaned_data['sex']
        edubackground = self.cleaned_data['edubackground']
        banknum = self.cleaned_data['banknum']
        user = User.objects.create_user(username, email, password)
        user.is_active=False#在进行邮箱验证之后，再激活用户
        user.save()
        userprofile = CITIS_users(utype=usertype,age=age,gender=sex, phonenum=phoneNum,educationback=edubackground,authuser_id=user.id)
        userprofile.save() 
        coreprofile = Profile(user_id = user.id,role=usertype,location=email,birthdate='1992-08-07',bankaccount=banknum,phone=phoneNum,sex=sex,edubackground=edubackground)
        coreprofile.save()

    
