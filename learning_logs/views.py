# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request,'learning_logs/index.html')

def admin(request):
    return HttpResponseRedirect(reverse('/admin'))

# def check_topic_owner(request,topic):
#     if topic.owner==request.user:
#         return True
#     else:
#         return False
    

@login_required #run it before use topics func, checking if the user is login or not.Using it to redirect to login.html
def topics(request):
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')#Only showing user's own content
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner!=request.user:#protect user's every topic content
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}#将模板保存在上下文中
    return render(request,'learning_logs/topic.html',context) #将上下文传递给render

@login_required
def new_topic(request):
    if request.method!='POST':
        form=TopicForm()
    else:#form must use POST method
        form=TopicForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user #match new_topic to current user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))#get url
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if request.method!='POST':
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.owner=request.user #match new_entry to current user
            new_entry.topic=topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
    context={'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if topic.owner!=request.user:#protecting edit page 
        raise Http404

    if request.method!='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)