from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

app_name='userApp'

urlpatterns=[
    
    url(r'^login/$',login,{'template_name':'userApp/login.html'},name='login'),#登录
    url(r'^logout/$',views.logout_view,name='logout'),#登出
    url(r'^Userinfo/$',views.UserInfo_view,name='Userinfo'),#当前用户个人信息   
    url(r'^Usersinfo/$',views.allUsers_view,name='Usersinfo'),#当前系统除管理员外所有用户信息
    url(r'^register/$',views.RegisterView.as_view(),name='register'),#注册新用户
    url(r'^modify_user/(?P<U_id>\d+)/$',views.modify_user,name='modify_user'),#修改用户信息
    url(r'^delete_user/$',views.delete_user,name='delete_user'),#修改用户信息
    url(r'^save_modified_userinfo/$',views.save_modified_userinfo,name='save_modified_userinfo'),#保存修改用户信息
    url(r'^searchusers/(?P<u_type>\d+)/(?P<u_id>\d+)/$',views.searchusers,name='searchusers'),#搜索框功能（用户管理界面）
    url(r'^account/activate/(?P<token>\w+)/$',views.active_user,name='active_user'),
    url(r'^getEchartData/$',views.getEchartData,name='getEchartData'),
    url(r'^tips/$',views.tips,name='tips')

]
