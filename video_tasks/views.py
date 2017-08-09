# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .forms import TaskForm, EntryForm
from .models import Task, Entry
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request,'video_tasks/index.html')

def admin(request):
    return HttpResponseRedirect(reverse('/admin'))

# def check_task_owner(request,task):
#     if task.owner==request.user:
#         return True
#     else:
#         return False
    

@login_required #run it before use Tasks func, checking if the user is login or not.Using it to redirect to login.html
def tasks(request):
    tasks=Task.objects.filter(owner=request.user).order_by('date_added')#Only showing user's own content
    context={'tasks':tasks}
    return render(request,'video_tasks/tasks.html',context)

@login_required
def task(request,task_id):
    task=Task.objects.get(id=task_id)
    if task.owner!=request.user:#protect user's every task content
        raise Http404
    entries=task.entry_set.order_by('-date_added')
    context={'task':task,'entries':entries}#将模板保存在上下文中
    return render(request,'video_tasks/task.html',context) #将上下文传递给render

@login_required
def new_task(request):
    if request.method!='POST':
        form=TaskForm()
    else:#form must use POST method
        form=TaskForm(request.POST)
        if form.is_valid():
            new_task=form.save(commit=False)
            new_task.owner=request.user #match new_task to current user
            new_task.save()
            return HttpResponseRedirect(reverse('video_tasks:tasks'))#get url
    context={'form':form}
    return render(request,'video_tasks/new_task.html',context)

@login_required
def new_entry(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method!='POST':
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.owner=request.user #match new_entry to current user
            new_entry.task=task
            new_entry.save()
            return HttpResponseRedirect(reverse('video_tasks:task',args=[task_id]))
    context={'task':task,'form':form}
    return render(request,'video_tasks/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    task=entry.task
    if task.owner!=request.user:#protecting edit page 
        raise Http404

    if request.method!='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('video_tasks:task',args=[task.id]))
    context={'entry':entry,'task':task,'form':form}
    return render(request,'video_tasks/edit_entry.html',context)