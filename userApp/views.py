# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from userApp.forms import RegisterForm
from .models import *
from video_tasks.models import *
from learning.core.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponse
from random import Random
from learning.settings import EMAIL_FROM
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.backends import ModelBackend  
from django.contrib.auth.tokens import default_token_generator
import json

def login_view(request):
    user = request.user
    user_profile = CITIS_users.objects.get(authuser_id = user.id)
    return render(request,"userApp/login.html",{'user':user,'user_profile':user_profile})
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('video_tasks:testindex'))

@login_required
def UserInfo_view(request):
    #user = User.objects.all() 
    #return render(request,"userApp/user_info.html",{'user':user})
    user = request.user
    user_profile = Profile.objects.get(user_id = user.id)
    user_records=User_Records.objects.filter(user_id=user.id)
    total_count = User_Records.objects.filter(user_id=user.id).count()
    accept_count = User_Records.objects.filter(Q(user_id=user.id),Q(status=1)).count()
    reject_count = User_Records.objects.filter(Q(user_id=user.id),Q(status=0),Q(appeal=-1)).count()
    remain_count = total_count-accept_count-reject_count

    #return render(request,"userApp/index_chart.html",{'user':user,'user_profile':user_profile})
    return render(request,"userApp/user_info_withchart.html",{'user':user,'user_profile':user_profile,'total_count':total_count,'accept_count':accept_count,'reject_count':reject_count,'remain_count':remain_count})

@login_required
def getEchartData(request):
    user = request.user
    total_count = User_Records.objects.filter(user_id=user.id).count()
    accept_count = User_Records.objects.filter(Q(user_id=user.id),Q(status=1)).count()
    reject_count = User_Records.objects.filter(Q(user_id=user.id),Q(status=0),Q(appeal=-1)).count()
    remain_count = total_count-accept_count-reject_count
    #list={'total_count':total_count,'accept_count':accept_count,'reject_count':reject_count,'remain_count':remain_count}
    list={"list1":[{"name":"total_count","value":total_count},{"name":"accept_count","value":accept_count},{"name":"reject_count","value":reject_count},{"name":"remain_count","value":remain_count}]}
    return HttpResponse(json.dumps(list),content_type="application/json")

@login_required
def allUsers_view(request):
    #users = User.objects.filter(is_superuser = 0) #非超级用户
    
    user_profiles = Profile.objects.all()
    profile1 = Profile.objects.filter(role='Annoter')
    a_users=[]
    for pro in profile1:
        user = User.objects.get(id = pro.user_id)
        a_user={"id":user.id,"username":user.username,"email":user.email,"role":pro.role,"phone":pro.phone}
        a_users.append(a_user)
    profile2 = Profile.objects.filter(role='Auditor')
    b_users=[]
    for pro in profile2:
        user = User.objects.get(id = pro.user_id)
        b_user={"id":user.id,"username":user.username,"email":user.email,"role":pro.role,"phone":pro.phone}
        b_users.append(b_user)   
    profile3 = Profile.objects.filter(role='Valuator')
    c_users=[]
    for pro in profile3:
        user = User.objects.get(id = pro.user_id)
        c_user={"id":user.id,"username":user.username,"email":user.email,"role":pro.role,"phone":pro.phone}
        c_users.append(c_user)
    paginator1 = Paginator(a_users,5)
    page1 = request.GET.get('page1',1) 
    print(page1)
    currentpage1 = int(page1)  
    try:
            annoters = paginator1.page(page1)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            annoters = paginator1.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            annoters = paginator1.page(paginator1.num_pages)       
            
    paginator2 = Paginator(b_users,5)
    page2 = request.GET.get('page2',1)
    currentpage2 = int(page2)  
    try:
            auditors = paginator2.page(page2)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            auditors = paginator2.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            auditors = paginator2.page(paginator2.num_pages)
            
    paginator3 = Paginator(c_users,5)
    page3 = request.GET.get('page3',1)
    currentpage3 = int(page3)  
    try:
            valuators = paginator3.page(page3)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            valuators = paginator3.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            valuators = paginator3.page(paginator3.num_pages)        
            
    return render(request,"userApp/users_info.html",{'user_profiles':user_profiles,'annoters':annoters,'auditors':auditors,'valuators':valuators})
    #return render(request,"userApp/testusers.html",{'users':users,'user_profiles':user_profiles,'annoters':annoters,'auditors':auditors,'valuators':valuators})


def modify_user(request,U_id):
    user = User.objects.get(id = U_id)
    return render(request,"userApp/modify_user.html",{'user':user})

def delete_user(request):
    u_ids = request.POST.getlist('userid')
    print(u_ids)
    for u_id in u_ids:
        user = User.objects.get(id=u_id)
        user.delete()
    return HttpResponse("success")

def save_modified_userinfo(request):
    U_id = request.POST.get('userid')
    print('111')
    print(U_id)
    print('222')
    user = User.objects.get(id = U_id)
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.profile.phone = request.POST.get('phone')
    user.save()
    user.profile.save()
    #return render(request,"userApp/user_info.html")
    #return render(request,"modify_user.html")
    return HttpResponse("success")

def searchusers(request,u_type,u_id): 
    user_profiles = Profile.objects.all()
    profile1 = []
    profile2 = []
    profile3 = []
    print(u_type)
    print(u_id)
    if u_type=='1':    
        print('hi1')    
        profile1 = Profile.objects.filter(Q(role='Annoter'),Q(user_id=u_id))
        profile2 = Profile.objects.filter(role='Auditor') 
        profile3 = Profile.objects.filter(role='Valuator')
    elif u_type =='2':
        profile1 = Profile.objects.filter(role='Annoter')
        profile2 = Profile.objects.filter(Q(role='Auditor'),Q(user_id=u_id))
        profile3 = Profile.objects.filter(role='Valuator')
    elif u_type == '3':
        profile1 = Profile.objects.filter(role='Annoter')
        profile2 = Profile.objects.filter(role='Auditor') 
        profile3 = Profile.objects.filter(Q(role='Valuator'),Q(user_id=u_id))
    
    
    a_users=[]
    for pro in profile1:
        user = User.objects.get(id = pro.user_id)
        a_user={"id":user.id,"username":user.username,"email":user.email,"role":pro.role,"phone":pro.phone}
        a_users.append(a_user)   
    b_users=[]
    for pro in profile2:
        user = User.objects.get(id = pro.user_id)
        b_user={"id":user.id,"username":user.username,"email":user.email,"role":pro.role,"phone":pro.phone}
        b_users.append(b_user)    
    c_users=[]
    for pro in profile3:
        user = User.objects.get(id = pro.user_id)
        c_user={"id":user.id,"username":user.username,"email":user.email,"role":pro.role,"phone":pro.phone}
        c_users.append(c_user)
    paginator1 = Paginator(a_users,5)
    page1 = request.GET.get('page1',1) 
    currentpage1 = int(page1)  
    try:
            annoters = paginator1.page(page1)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            annoters = paginator1.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            annoters = paginator1.page(paginator1.num_pages)       
            
    paginator2 = Paginator(b_users,5)
    page2 = request.GET.get('page2',1)
    currentpage2 = int(page2)  
    try:
            auditors = paginator2.page(page2)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            auditors = paginator2.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            auditors = paginator2.page(paginator2.num_pages)
            
    paginator3 = Paginator(c_users,5)
    page3 = request.GET.get('page3',1)
    currentpage3 = int(page3)  
    try:
            valuators = paginator3.page(page3)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            valuators = paginator3.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            valuators = paginator3.page(paginator3.num_pages)        
            
    return render(request,"userApp/users_info.html",{'user_profiles':user_profiles,'annoters':annoters,'auditors':auditors,'valuators':valuators})


class RegisterView(FormView):
    template_name = 'userApp/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('video_tasks:index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')   
        email = form.cleaned_data.get('email')     
        user = authenticate(username=username, password=password)#authenticate接收参数用户名和密码，并且在用户名和密码合法的情况下返回User对象
        
        #验证邮箱的手段
        send_register_email(username,email,"register")
        #login(self.request, user)
        #return super(RegisterView, self).form_valid(form)
        return HttpResponseRedirect('/userApp/tips')

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_register_email(username,email, send_type="register"):
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(16)
    email_record.verify_code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "视频标记系统注册激活链接"
        #email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        email_body = "\n".join([u'{0},欢迎加入'.format(username),u'请访问该链接，完成用户验证:','/'.join(['http://127.0.0.1:8000/userApp/account/activate',code])])
        #email_body = "\n".join([u'{0},欢迎加入'.format(username),u'请访问该链接，完成用户验证:','/'.join(["{% url 'userApp.views.active_user' %}",code]),u'fangwen'])
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
def active_user(request,token):   
    all_records = EmailVerifyRecord.objects.filter(verify_code=token)
    if all_records:
        for record in all_records:
            email = record.email
            # 通过邮箱查找到对应的用户
            user = User.objects.get(email=email)
            # 激活用户
            user.is_active = True
            user.save()
    return HttpResponseRedirect('/testindex') 


def tips(request):
    return render(request,"userApp/tips.html")


#待删

# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()
