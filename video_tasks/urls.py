'''defining the app video_tasks URL'''
from django.conf.urls import  url 
from django.contrib import admin
from django.contrib.auth.views import login
from . import views

app_name = 'video_tasks'
urlpatterns = [
    url(r'^$',login,{'template_name':'userApp/login.html'},name='index'), #登录链接
    url(r'^testindex/$',views.testindex,name='testindex'), #首页链接
    url(r'^web_index/$',views.web_index,name='web_index'), #首页链接
    url(r'^welcome/$',views.welcome,name='welcome'), #根据用户身份进入不同系统
    url(r'^admin/', admin.site.urls),#管理员网站
    
    url(r'^auditor_videoupload/$',views.auditor_videoupload,name='auditor_videoupload'), #上传视频
    url(r'^auditor_videouploaded/$',views.auditor_videouploaded,name='auditor_videouploaded'), 
    
    #加载视频中用到的函数
    url(r'^ann/$',views.ann,name='ann'),
    url(r'^ann/server/getjob/$',views.getjob,name='getjob'),
    url(r'^ann/server/getboxesforjob/(?P<J_id>\d+)/$',views.getboxesforjob,name='getboxesforjob'),
    url(r'^ann/server/savejob/(?P<J_id>\d+)/$',views.savejob,name='savejob'),
    
    url(r'^changejobstatus/$',views.changejobstatus,name='changejobstatus'),#改变任务或者视频的状态
    url(r'^auditor_task/$',views.auditor_task,name='auditor_task'),#根据审核员的‘接受’或拒绝评价，修改任务状态
    url(r'^dump/$',views.dump,name='dump'),#视频导出   
    url(r'^annotertasklist/$',views.annoter_tasks,name='annoter_tasks'),#标记任务列表
    url(r'^auditortasklist/$',views.auditor_tasks,name='auditor_tasks'),#审核任务列表
    url(r'^valuatortasklist/$',views.valuator_tasks,name='valuator_tasks'),#评价任务列表
    url(r'^dumptasklist/$',views.dump_tasks,name='dump_tasks'),#导出任务列表
    url(r'^admin_welcome/$',views.admin_welcome,name='admin_welcome'),#管理员主界面
    url(r'^manage_video/$',views.manage_video,name='manage_video'),#视频管理主界面
    url(r'^published_videos/$',views.published_videos,name='published_videos'),#已发布视频列表界面
    url(r'^unpublished_videos/$',views.unpublished_videos,name='unpublished_videos'),#未发布视频列表界面
    url(r'^manage_job/$',views.manage_job,name='manage_job'),#任务管理主界面
    url(r'^manage_data/$',views.manage_data,name='manage_data'),#数据管理主界面
    url(r'^finished_tasks/$',views.finished_tasks,name='finished_tasks'),#已完成任务界面
    url(r'^error_tasks/$',views.error_tasks,name='error_tasks'),#失败任务界面
    url(r'^suc_tasks/$',views.suc_tasks,name='suc_tasks'),#成功任务界面
    url(r'^applytasklist/$',views.apply_annoter_tasks,name='apply_tasks'),#标记员申领标记任务列表
    url(r'^apply_tasks/$',views.apply_tasks,name='apply_tasks'),#申领任务界面（审核员和评价员）
    url(r'^searchvideos/(?P<action>\w+)/(?P<content>\w+)/$',views.searchvideos,name='searchvideos'),#搜索
    url(r'^appeal_tasks/$',views.appeal_tasks,name='appeal_tasks'),#可申诉任务
    url(r'^ready_appeal_tasks/$',views.ready_appeal_tasks,name='ready_appeal_tasks'),#可申领待处理申诉任务
    url(r'^access_appeal/$',views.access_appeal,name='access_appeal'),#处理待申诉任务
    url(r'^handle_appeal_tasks/$',views.handle_appeal_tasks,name='handle_appeal_tasks'),#待处理申诉任务
    url(r'^handle_appeal/$',views.handle_appeal,name='handle_appeal'),#处理待申诉任务
    url(r'^handled_appeal_tasks/$',views.handled_appeal_tasks,name='handled_appeal_tasks'),#已处理的申诉任务
    url(r'^introduction/$',views.introduction,name='introduction'),#test for introduction ui
    url(r'^test/$',views.test,name='test'),#test for link to the environment
    url(r'^testforlink/$',views.testforlink,name='testforlink'),#testforlink
    url(r'^img_eval/$',views.img_eval,name='img_eval'),#img_eval
]
