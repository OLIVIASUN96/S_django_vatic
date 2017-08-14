'''defining the app video_tasks URL'''
from django.conf.urls import  url 
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    # url(r'^admin',views.admin,name='admin'), #admin change
    url(r'^admin/', admin.site.urls),
    url(r'^tasks/$',views.tasks,name='tasks'),
    url(r'^tasks/(?P<task_id>\d+)/$',views.task,name='task'),
    url(r'^new_task/$',views.new_task,name='new_task'),
    url(r'^new_entry/(?P<task_id>\d+)/$',views.new_entry,name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry'),
]
