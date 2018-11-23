# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect, Http404
#from django.core.urlresolvers import reverse
from django.urls import reverse
#from .forms import TaskForm, EntryForm
from .models import *
from django.contrib.auth.decorators import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from pyvision.vision import ffmpeg
from sqlalchemy.sql.elements import Null
import json
from django.template.loader import get_template
from userApp.models import *
from learning.core.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pyvision.vision.track import interpolation
from django.db.models import Q
import cv2
import jpype



logger = logging.getLogger("CITIS.database")

Base = declarative_base()

try:
    import config
except ImportError:
    session = None
    Session = None
else:
    engine = create_engine(config.database, pool_recycle = 3600)

    Session = sessionmaker(bind=engine)
    session = scoped_session(Session)



# Create your views here.



#申领视频 publish wei1的视频 然后标注
@login_required
def apply_annoter_tasks(request):
    videos = Video.objects.filter(Q(publish=1)&Q(applied_id=-1))#已发布且未被申领的视频
    paginator = Paginator(videos,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)   
    return render(request,'video_tasks/apply_annotation_tasks.html',{'jobs':jobs})

@login_required
def apply_tasks(request):
    user = request.user
    job_list=[]
    tasks=[]
    if user.profile.role == "Auditor":
        job_list = Job.objects.filter(Q(status = 2)&Q(auditor_id=-1))
    elif user.profile.role == "Valuator":
        job_list = Job.objects.filter(Q(status = 3)&Q(valuator_id=-1))
    for job in job_list:
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        print(video.id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/apply_tasks.html',{'jobs':jobs})

@login_required
def appeal_tasks(request):
    records = []
    user = request.user
    job_list=[]
    tasks=[]
    records = User_Records.objects.filter(Q(user_id=user.id),Q(appeal=1))
    for record in records:
        job = Job.objects.get(id = record.job_id)
        job_list.append(job)    
    for job in job_list:
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        print(video.id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/appeal_tasks.html',{'jobs':jobs})

@login_required
def handled_appeal_tasks(request):
    records = []
    user = request.user
   
    tasks=[]
    records = User_Records.objects.filter(Q(user_id=user.id),Q(appeal=-1))
    for record in records:
        job = Job.objects.get(id = record.job_id)
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":record.status,"appeal":record.status}
        tasks.append(task)

    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/handled_appeal_tasks.html',{'jobs':jobs})

@login_required
def ready_appeal_tasks(request):
    records = []
    user = request.user
    job_list=[]
    tasks=[]
    records = User_Records.objects.filter(Q(appeal=2))
    for record in records:
        job = Job.objects.get(id = record.job_id)
        job_list.append(job)    
    for job in job_list:
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        print(video.id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/ready_appeal_tasks.html',{'jobs':jobs})




@login_required
def handle_appeal_tasks(request):
    records = []
    user = request.user
    job_list=[]
    tasks=[]
    records = User_Records.objects.filter(Q(appeal=3),Q(user_id=user.id))
    
    for record in records:
        job = Job.objects.get(id = record.job_id)
        job_list.append(job)    
    for job in job_list:
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        print(video.id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/handle_appeal_tasks.html',{'jobs':jobs})


@login_required
def annoter_tasks(request):
    #job_list = Job.objects.filter(Q(istraining = 1)|Q(istraining = 2))
    user = request.user
    video_list = Video.objects.filter(Q(applied_id = user.id)&Q(status=1),Q(publish=1))#被当前标注员申领过的视频
    print(video_list)
    segment_list = []
    for video in video_list:
        segments = Segment.objects.filter(video_id = video.id)
        for segment in segments:
            segment_list.append(segment)
    job_list=[]
    for segment in segment_list:
        print(segment.id)
        try:
            job = Job.objects.get(Q(segment_id=segment.id)&Q(status=1))
            job_list.append(job)
        except:
            pass
        
    tasks = []
    for job in job_list:       
        segment = Segment.objects.get(id=job.segment_id)            
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        print(video.id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)

    return render(request,'video_tasks/annotator_task_list.html',{'jobs':jobs})

@login_required
def auditor_tasks(request):
    #job_list = Job.objects.filter(istraining = 3)
    user = request.user
    job_list = Job.objects.filter(Q(auditor_id = user.id)&Q(status=2))
    tasks = []
    for job in job_list:
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    return render(request,'video_tasks/auditor_task_list.html',{'jobs':jobs})

@login_required
def valuator_tasks(request):
    user = request.user
    job_list = Job.objects.filter(Q(valuator_id = user.id),Q(status=3))
    tasks = []
    for job in job_list:
        segment = Segment.objects.get(id=job.segment_id)
        video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start}
        tasks.append(task)
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
   
    #jobs = jobs.join(Segment).join(Video)
    return render(request,'video_tasks/valuator_task_list.html',{'jobs':jobs})

@login_required
def dump_tasks(request):
    #job_list = Job.objects.all()
    #job_list = Job.objects.filter(istraining = 4 )
    #videos=[]
    #for job in job_list:
       # segment = Segment.objects.get(id=job.segment_id)
        #video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
        
    videos = Video.objects.filter(status = 4)
    #videos.append(video)
    paginator = Paginator(videos,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
   
    #jobs = jobs.join(Segment).join(Video)
    
 
    return render(request,'video_tasks/dump_task_list.html',{'jobs':jobs})



    



#用户登录根据用户角色（管理员、标记员、审议员、评价员）进入不同的页面
@login_required
def welcome(request):
    user = request.user
    if user.is_superuser == 1:
        return HttpResponseRedirect('/admin_welcome')
    #user_profile = CITIS_users.objects.get(authuser_id = user.id)
    #根据用户角色进入不同的页面
    core_profile = Profile.objects.get(user_id = user.id)
    if core_profile.role == 'Annoter': #annoter
        return HttpResponseRedirect('/annotertasklist')
    elif core_profile.role == 'Auditor':#审计员
        return HttpResponseRedirect('/auditortasklist')
    elif core_profile.role == 'Valuator':#评议员
        return HttpResponseRedirect('/valuatortasklist')


    


@login_required
def ann(request):
    J_id = request.GET.get('id')
    verified = request.GET.get('hitid')
    t = get_template("video_tasks/ann.html")
    html = t.render({"id":J_id,"hitid":verified})
    #return render(request,'video_tasks/ann.html',json.dumps({"id":J_id,"hitid":verified}))
    return HttpResponse(html)
# id hitid 

@login_required
def auditor_videoupload(request):
     return render(request,'video_tasks/auditor_videoupload.html')



#上传视频
#用户传参，参数可用于操作
@login_required
def auditor_videouploaded(request):
    videonames= request.POST.getlist('myfiles')
    labels = request.POST.getlist('labels')
    description = request.POST.get('description')
    print("description")
    print(description)
    start_frame = 0
    stop_frame = None
    length = 300
    overlap = 20
    per_object_bonus = None
    completion_bonus = None
    #print(os.path.abspath('.'))
    print("hi videonames")
    print(videonames)
    print(labels)
    error_video = 0#上传不成功视频的数量
    
    for videoname in videonames:
        identifier = videoname       
    #####################video extract#####################
        try:
            os.makedirs(os.path.abspath('.')+"/data/output/"+identifier)#目录创建成功         
        except:
            pass
        sequence = ffmpeg.extract(os.path.abspath('.')+"/data/video/"+videoname)#切分视频
        try:
            for frame, image in enumerate(sequence):
                if frame % 100 == 0:
                    print ("Decoding frames {0} to {1}"
                       .format(frame, frame + 100))
                    print(os.path.abspath('.')+"/data/output/"+identifier)
                #if not args.no_resize:
                    #image.thumbnail((args.width, args.height), Image.BILINEAR)
                path = Video.getframepath(frame, os.path.abspath('.')+"/data/output/"+identifier)
                try:
                    print("pathaaa" + path)
                    image.save(path)#将图像保存到指定的流中               
                except IOError:
                    os.makedirs(os.path.dirname(path))
                    image.save(path)
        except:
            #if not args.no_cleanup:
                print("Aborted. Cleaning up...")
                shutil.rmtree(os.path.abspath('.')+"/data/output/"+identifier)#递归删除目录树
         #raise
    #####################video load###############################
    
        #train_with = False #界面上要加这个按钮
    
        print("Checking integrity...")
        # read first frame to get sizes
        path = Video.getframepath(0, os.path.abspath('.')+"/data/output/"+identifier)
        try:
            im = Image.open(path)
        except IOError:
            print("Cannot read {0}".format(path))
            error_video = error_video+1
            continue
        width, height = im.size
        print("Searching for last frame...")
        # search for last frame
        toplevel = max(int(x)
            for x in os.listdir(os.path.abspath('.')+"/data/output/"+identifier))
        secondlevel = max(int(x)
            for x in os.listdir("{0}/{1}".format(os.path.abspath('.')+"/data/output/"+identifier, toplevel)))
        maxframes = max(int(os.path.splitext(x)[0])
            for x in os.listdir("{0}/{1}/{2}"
            .format(os.path.abspath('.')+"/data/output/"+identifier, toplevel, secondlevel))) + 1
        
        print("Found {0} frames.".format(maxframes))    
    
    # can we read the last frame?          
        path = Video.getframepath(maxframes - 1, os.path.abspath('.')+"/data/output/"+identifier)
        try:
            im = Image.open(path)
        except IOError:
            print("Cannot read {0}".format(path))
            error_video = error_video+1
            continue
    
    # check last frame sizes
        if im.size[0] != width and im.size[1] != height:
            print("First frame dimensions differs from last frame")
            error_video = error_video+1
            continue
    
    #如果该视频已经存在了，就不上传了
        if Video.objects.filter(slug = identifier).count():
            print("Video {0} already exists!".format(identifier))
            error_video = error_video+1
            continue
    
    #被训练的那个参数晚点儿再加
    
    # create video
        video = Video(slug = identifier,
                  location = os.path.abspath('.')+"/data/output/"+identifier, 
                  width = width,
                  height = height,
                  totalframes = maxframes,
                  skip = 0,
                  perobjectbonus = 0,
                  completionbonus = 0,
                  #trainwith = None,
                  isfortraining = 0,
                  blowradius = 0,
                  description = description)
    
        video.save()
    
    #创建hit_group
        group = HITGroup(title='Video annotation',
                     description = 'Draw boxes around objects moving around in a video.',
                     duration = 21600,
                     lifetime = 1209600,
                     cost = 0.05,
                     keywords = 'video,annotation,computer,vision',
                     height = height,
                     donation = 0,
                     offline = 0,)
        group.save()
    
        print("Binding labels and attributes...")
    
    # create labels and attributes
        labelcache = {}
        attributecache = {}
        lastlabel = None
    #if attributes is None:
        #print("Cannot assign an attribute without a label!")
        #return
    
        for la in labels:
            label = Label(text=la,video=video)
            label.save()
            if la =='person':
                attribute1 = Attribute(text = 'standing',label=label)   
                attribute1.save()
                attribute2 = Attribute(text = 'walking',label=label)   
                attribute2.save()
                attribute3 = Attribute(text = 'running',label=label)   
                attribute3.save()
            elif la =='car':
                attribute1 = Attribute(text = 'standing',label=label)   
                attribute1.save()            
                attribute2 = Attribute(text = 'running',label=label)   
                attribute2.save()
    
        print("Creating symbolic link...")
    #symlink = os.path.abspath('.')+"/video_tasks/"+"public/frames/{0}".format(identifier)
        symlink = os.path.abspath('.')+"/video_tasks/"+"static/video_tasks/frames/{0}".format(identifier)#静态资源放在static下面可以加载的出来
        try:
            os.remove(symlink)
        except:
            pass
        os.symlink(os.path.abspath('.')+"/data/output/"+identifier,symlink)
        print("Creating segments...")
    # create shots and jobs 
        startframe = start_frame
        stopframe = stop_frame
        if not stopframe:
            stopframe = video.totalframes - 1
        for start in range(startframe, stopframe, length):
            stop = min(start + length + overlap + 1,
                           stopframe)
            segment = Segment(start = start,
                          stop = stop,
                          video = video)
            segment.save()
            job = Job(segment = segment)
            job.save()    
        
            hit = HIT(hitslug = identifier,
                  group = group,
                  description = identifier,
                  type = 'jobs'
            )
            hit.save()
        
    
       
    
    #if per_object_bonus:
       # group.schedules.append(
            #PerObjectBonus(amount = per_object_bonus))
    #if  completion_bonus:
        #group.schedules.append(
            #CompletionBonus(amount = completion_bonus))

    #group.add()
        print("Video loaded and ready for publication.")
    if error_video ==0:
        return HttpResponse("success")
    else:
        return HttpResponse("error")
    #return render(request,'video_tasks/auditor_videoupload.html')


# def admin(request):
#     return HttpResponseRedirect(reverse('/admin'))

# def check_task_owner(request,task):
#     if task.owner==request.user:
#         return True
#     else:
#         return False
    



#getjob
@login_required
def getjob(request):    
    J_id = request.GET.get('id')
    print(J_id)
    hitid = request.GET.get('hitid')
    
    job = Job.objects.get(id=J_id)
    logger.debug("Found job {0}".format(job.id))
    
    #if hitid and Video.objects.get(id=(Segment.objects.get(id=job.segment_id).video_id)).isfortraining
    #if hitid and job.segment.video.trainwith:
        # swap segment with the training segment
        #training = True
        #segment = job.segment.video.trainwith.segments[0]
        #logger.debug("Swapping actual segment with training segment")
   # else:
    training = False
    print("hi there")
    print(job.segment_id)
    segment = Segment.objects.get(id=job.segment_id)
        #segment = Segment.objects.get(id=7)
        
    video = Video.objects.get(id = segment.video_id)
    #labels = dict((l.id, l.text) for l in video.labels)   
    labels = dict((l.id, l.text) for l in Label.objects.filter(video_id = video.id))
    
    attributes = {}
    #for label in video.labels:
        #attributes[label.id] = dict((a.id, a.text) for a in label.attributes)
    for label in Label.objects.filter(video_id = video.id):
        attributes[label.id] = dict((a.id, a.text) for a in Attribute.objects.filter(label_id = label.id))
    logger.debug("Giving user frames {0} to {1} of {2}".format(video.slug,
                                                              segment.start,
                                                              segment.stop))
    
    data = {"start":       segment.start,
            "stop":         segment.stop,
            "slug":         video.slug,
            "width":        video.width,
            "height":       video.height,
            "skip":         video.skip,
            "perobject":    video.perobjectbonus,
            "completion":   video.completionbonus,
            "blowradius":   video.blowradius,
            "jobid":        job.id,
            "training":     int(training),
            "labels":       labels,
            "attributes":   attributes}   
    
    data1 = json.dumps(data,separators=(',',':'))
    return HttpResponse(data1)
    #t = get_template("video_tasks/ann.html")
   # html = t.render({"data":data})
    #return render(request,'video_tasks/ann.html',json.dumps({"id":J_id,"hitid":verified}))
    #return HttpResponse(html)
                                                       
    #data1 = json.dumps(data,separators=(',',':'))   


#getboxesforjob
@login_required    
def getboxesforjob(request,J_id): 
    
    #J_id = request.GET.get('id')
    job = Job.objects.get(id=J_id)
    
    result = []
    for path in Path.objects.filter(job = job.id):       
        attrs=[]
        for attr in Attribute.objects.filter(label_id = path.label_id):
            attr_annos = AttributeAnnotation.objects.get(Q(path=path.id),Q(attribute=attr.id))
            for attr_anno in attr_annos:
               a = [attr.id,attr_anno.frame,attr_anno.value]
               attrs.append(a)
        #attrs = [(x.id, Segment.objects.get(id = job.segment_id).start, 'true') for x in Attribute.objects.filter(label_id = path.label_id)]
        result.append({"label": path.label_id,
                       "boxes": [tuple(x) for x in path.getboxes()], #tuple好像是强制转换成tuple类型的意思
                       #"boxes": [json.dumps(x,separators=(',',':')) for x in path.getboxes()],
                       "attributes": attrs})
    result1 = json.dumps(result,separators=(',',':'))
    return HttpResponse(result1)



def readpaths(tracks,J_id):
    paths = []
    logger.debug("Reading {0} total tracks".format(len(tracks)))

    for label, track, attributes in tracks:
        path = Path()
        #path.label = session.query(Label).get(label)
        #path.labelid_id = Label.objects.get(id = label.id)
        path.label_id = label
        path.job_id = J_id
        logger.debug("Received a {0} track".format(path.label_id))
        path.save()
        print("path save\n")
        visible = False
        for frame, userbox in track.items():
            print(frame)
            box = Box(pathid_id = path.id)
            box.xtl = max(int(userbox[0]), 0)
            box.ytl = max(int(userbox[1]), 0)
            box.xbr = max(int(userbox[2]), 0)
            box.ybr = max(int(userbox[3]), 0)
            box.occluded = int(userbox[4])
            box.outside = int(userbox[5])
            box.frame = int(frame)
            if not box.outside:
                visible = True
            box.save()
            print("box save\n")
            logger.debug("Received box {0}".format(str(box.getbox())))

        if not visible:
            logger.warning("Received empty path! Skipping")
            continue

        for attributeid, timeline in attributes.items():
            #attribute = session.query(Attribute).get(attributeid)
            attribute = Attribute.objects.get(id = attributeid)
            for frame, value in timeline.items():
                aa = AttributeAnnotation()
                aa.attribute_id = attribute.id
                aa.frame = frame
                aa.value = value
                aa.path_id = path.id
                aa.save()
                print("attributeannotation save\n")
        paths.append(path)
    return paths

#保存标记
@login_required
def savejob(request,J_id):
    tracks = json.loads(request.body.decode('utf-8'))     
    job = Job.objects.get(id = J_id)    
    for path in Path.objects.filter(job=job.id):
        path.delete()    
    paths = readpaths(tracks,J_id)
    return render(request,'video_tasks/ann.html')


#保存完第一帧标记之后，系统先自动跟踪对象标记
#def auto_anno(request,J_id):
 #   job = Job.objects.get(id = J_id) 
  #  segment = Segment.objects.get(id=job.segment_id)
   # video = Video.objects.get(id = segment.video_id)
    #I = Image.open(video.location)#this location is not the exactly location of the first image, need to change 
    #L = I.convert('L') #将RGB图像转换为灰度图像
    
    #read the file and get the bounding box
    #----read the file----
   # initial_box = open('init.txt','r')
    #boxlines = initial_box.read().splitlines()
    #x = 0
    #y = 0
    #w = 0
    #h = 0
    #for line in boxlines:
     #   line = line.split(',')	
	#x = line[0]
	#y = line[1]
	#w = line[2]-line[0]
	#h = line[3]-line[1]
  #  box = Rect(x,y,w,h)#the first bounding box including the tracking object
    
    #the next step: using the bounding box and the first frame to init the TLD system
    #not find the corresponding function yet, still have to look this afternoon. find it! in the file TLD.cpp(void TLD::init(xxx)) now figure out how to implement complicated logic problems using the django framework. It's quite difficult.

class DumpCommand():
    #parent = argparse.ArgumentParser(add_help=False)
    #parent.add_argument("slug")
    #parent.add_argument("--merge", "-m", action="store_true", default=False)
    #parent.add_argument("--merge-threshold", "-t",
                        #type=float, default = 0.5)
   # parent.add_argument("--worker", "-w", nargs = "*", default = None)

    class Tracklet(object):
        def __init__(self, label, paths, boxes, workers):
            self.label = label
            self.paths = paths
            self.boxes = sorted(boxes, key = lambda x: x[4])
            self.workers = workers

        def bind(self):
            for path in self.paths:
                self.boxes = Path.bindattributes(path.attributes, self.boxes)

    def getdata(self, args):
        response = []
        video = session.query(Video).filter(Video.slug == args.slug)
        if video.count() == 0:
            print("Video {0} does not exist!".format(args.slug))
            raise SystemExit()
        video = video.one()

        if args.merge:
            for boxes, paths in merge.merge(video.segments, 
                                            threshold = args.merge_threshold):
                workers = list(set(x.job.workerid for x in paths))
                tracklet = DumpCommand.Tracklet(paths[0].label.text,
                                                paths, boxes, workers)
                response.append(tracklet)
        else:
            for segment in video.segments:
                for job in segment.jobs:
                    if not job.useful:
                        continue
                    worker = job.workerid
                    for path in job.paths:
                        tracklet = DumpCommand.Tracklet(path.label.text,
                                                        [path],
                                                        path.getboxes(),
                                                        [worker])
                        response.append(tracklet)

        if args.worker:
            workers = set(args.worker)
            response = [x for x in response if set(x.workers) & workers]

        interpolated = []
        for track in response:
            path = vision.track.interpolation.LinearFill(track.boxes)
            tracklet = DumpCommand.Tracklet(track.label, track.paths,
                                            path, track.workers)
            interpolated.append(tracklet)
        response = interpolated

        for tracklet in response:
            tracklet.bind()

        return video, response



#数据以pascal形式导出
@login_required  
def dump(request):    
    #获得数据
    print("hi dump")
    slugs = request.POST.getlist("slug")
    print(slugs)
    
    for slug in slugs:
        video = Video.objects.filter(slug=slug)
        response = []
        if video.count() == 0:
            print("Video {0} does not exist!".format(slug))
        video = Video.objects.get(slug=slug)
    
        #不考虑merge的情况
        for segment in Segment.objects.filter(video=video):
            for job in Job.objects.filter(segment=segment):
            #if not job.useful:
                #continue
            #worker = job.workerid
                worker = None
                for path in Path.objects.filter(job=job):
                    tracklet = DumpCommand.Tracklet(path.label,
                                                [path],
                                                path.getboxes(),
                                                [worker])
                    response.append(tracklet)
    
    #新添加
        interpolated = []
        result = []
        for track in response:
            for source,target in zip(track.boxes,(track.boxes)[1:]):
                print("target")
                print(target[4])
                print("source")
                print(source[4])
                if target[4] <= source[4]:
                    raise ValueError("Target frame must be greater than source frame "
        "(source = {0}, target = {1})".format(source.frame, target.frame))

                fdiff = float(target[4] - source[4])
                xtlr  = (target[0] - source[0]) / fdiff
                ytlr  = (target[1] - source[1]) / fdiff
                xbrr  = (target[2] - source[2]) / fdiff
                ybrr  = (target[3] - source[3]) / fdiff
                results=[]
            
            #3.30 刚把注释放出来
                for i in range(source[4], target[4] + 1):
                    off = i - source[4]
                    xtl = int(source[0] + xtlr * off)
                    ytl = int(source[1] + ytlr * off)
                    xbr = int(source[2] + xbrr * off)
                    ybr = int(source[3] + ybrr * off)
                    generated = int(i != source[4] and i != target[4])
                    lost = source[5] or target[5]
                    results.append((xtl, ytl, xbr, ybr,
                       i, 
                       lost,
                       source[8],
                       generated,
                       list(source[11])))
            
                tracklet = DumpCommand.Tracklet(track.label, track.paths,
                                            results, track.workers)
                interpolated.append(tracklet)
    
        response = interpolated

    #for tracklet in response:
        #tracklet.bind()
    ####
    
    
    #导出
    #folder = request.GET.get('folder')#导出后的文件夹位置 决定先确定一个文件夹的位置
        try:
            os.makedirs(os.path.abspath('.')+"/data/dump/"+slug)#目录创建成功         
        except:
            pass
        folder = os.path.abspath('.')+"/data/dump/"+slug
        video = video
        data = response
        difficultthresh = 100 #default = 100 先按默认值来
        skip = 1 #default = 1
        negdir = None #这个没有默认值
    
        byframe = {}
        for track in data:
            for box in track.boxes:
                if box[4] not in byframe:
                    byframe[box[4]] = []
                byframe[box[4]].append((box, track))
    
        hasit = {}
        allframes = range(0,video.totalframes,skip)
    
        try:
            os.makedirs("{0}/Annotations".format(folder))
        except:
            pass
        try:
            os.makedirs("{0}/ImageSets/Main/".format(folder))
        except:
            pass
        try:
            os.makedirs("{0}/JPEGImages/".format(folder))
        except:
            pass
    
        numdifficult = 0
        numtotal = 0

        pascalds = None
        allnegatives = set()
        if negdir:
            pascalds = vision.pascal.PascalDataset(negdir)
    
        print("Writing annotations...")    
        for frame in allframes:
            if frame in byframe:
                boxes = byframe[frame]
            else:
                boxes = []
        
            strframe = str(frame+1).zfill(6)
            filename = "{0}/Annotations/{1}.xml".format(folder, strframe)
            file = open(filename, "w")
            file.write("<annotation>")
            file.write("<folder>{0}</folder>".format(folder))
            file.write("<filename>{0}.jpg</filename>".format(strframe))
         
            isempty = True
            for box, track in boxes:
                print(box)
                if box[5]:
                    continue  
            
                isempty = False
                if track.label not in hasit:
                    hasit[track.label] = set()
                    hasit[track.label].add(frame)
            
                numtotal += 1

                #difficult = box.area < difficultthresh
                #if difficult:
                    #numdifficult += 1
                #difficult = int(difficult)

                file.write("<object>")
                file.write("<name>{0}</name>".format(track.label.text))
                file.write("<bndbox>")           
                file.write("<xmax>{0}</xmax>".format(box[2]))            
                file.write("<xmin>{0}</xmin>".format(box[0]))          
                file.write("<ymax>{0}</ymax>".format(box[3]))           
                file.write("<ymin>{0}</ymin>".format(box[1]))
                file.write("</bndbox>")            
                file.write("<difficult>{0}</difficult>".format(1))           
                file.write("<occluded>{0}</occluded>".format(box[6]))
                file.write("<pose>Unspecified</pose>")
                file.write("<truncated>0</truncated>")
                file.write("</object>")
            
            if isempty:
            # since there are no objects for this frame,
            # we need to fabricate one
                file.write("<object>")
                file.write("<name>not-a-real-object</name>")
                file.write("<bndbox>")
                file.write("<xmax>10</xmax>")
                file.write("<xmin>20</xmin>")
                file.write("<ymax>30</ymax>")
                file.write("<ymin>40</ymin>")
                file.write("</bndbox>")
                file.write("<difficult>1</difficult>")
                file.write("<occluded>1</occluded>")
                file.write("<pose>Unspecified</pose>")
                file.write("<truncated>0</truncated>")
                file.write("</object>")
            
            file.write("<segmented>0</segmented>")
            file.write("<size>")
            file.write("<depth>3</depth>")           
            file.write("<width>{0}</width>".format(video.width))
            file.write("<height>{0}</height>".format(video.height)) #好像是写反了 应该是video 的height 改成width
            file.write("</size>")
            file.write("<source>")
            file.write("<annotation>{0}</annotation>".format(video.slug))
            file.write("<database>vatic</database>")
            file.write("<image>vatic</image>")
            file.write("</source>")
            file.write("<owner>")
            file.write("<flickrid>vatic</flickrid>")
            file.write("<name>vatic</name>")
            file.write("</owner>")
            file.write("</annotation>")
            file.close()
        
        print("{0} of {1} are difficult".format(numdifficult, numtotal))
        print("Writing image sets...")
        for label, frames in hasit.items():
            filename = "{0}/ImageSets/Main/{1}_trainval.txt".format(folder,
                                                                    label)
            file = open(filename, "w")
            for frame in allframes:
                file.write(str(frame+1).zfill(6))
                file.write(" ")
                if frame in frames:
                    file.write("1")
                else:
                    file.write("-1")
                file.write("\n")
    
            file.close()
            train = "{0}/ImageSets/Main/{1}_train.txt".format(folder, label)
            shutil.copyfile(filename, train)
    
        filename = "{0}/ImageSets/Main/trainval.txt".format(folder)
        file = open(filename, "w")
        file.write("\n".join(str(x+1).zfill(6) for x in allframes))
        for neg in allnegatives:
            file.write("n{0}\n".format(neg))
        file.close()

        train = "{0}/ImageSets/Main/train.txt".format(folder)
        shutil.copyfile(filename, train)
        print("Writing JPEG frames...")
        for frame in allframes:
            strframe = str(frame+1).zfill(6)
            path = Video.getframepath(frame, video.location)
            dest = "{0}/JPEGImages/{1}.jpg".format(folder, strframe)
            try:
                os.unlink(dest)
            except OSError:
                pass
            os.link(path, dest)

        print("Done.")
    
    return HttpResponse('success')





#在用户申领，提交标注之后改变job的状态
@login_required     
def changejobstatus(request):
    #为发布状态 0  
    #发布状态 1
    #申领状态 2
    #提交状态 3
    #1审核通过4
    #1审核不通过2
    #2审核结果提交 5
    print("hi changejobstatus")
    Action = request.POST.get("Action")
    J_ids = request.POST.getlist("J_id")
    print(Action)
    print(J_ids)
    if Action=='publish':#发布状态修改成功
        for J_id in J_ids:
            video = Video.objects.get(id=J_id)
            video.publish = 1
            video.status = 1
            segments = Segment.objects.filter(video_id = video.id)
            for seg in segments:
                job = Job.objects.get(segment_id = seg.id)
                job.status = 1
                job.save()
            print(J_id)
            print("publish change status")
            video.save()
        return HttpResponse("success") 
    elif Action=='unpublish':
        for J_id in J_ids:
            video = Video.objects.get(id=J_id)
            video.publish = 0
            print(J_id)
            print("unpublish change status")
            video.save()  
        return HttpResponse("success")  
    
    elif Action=='apply':#申领视频
        user = request.user
        for J_id in J_ids:
            video = Video.objects.get(id=J_id)
            video.applied_id = user.id
            video.save()
            #存储用户操作记录
            segments = Segment.objects.filter(video_id=J_id)
            for seg in segments:
                job = Job.objects.get(segment_id=seg.id)
                obj = User_Records(user_id=user.id,job_id=job.id)
                obj.save()
            
        return HttpResponse('success')
    elif Action=='anno_finish':#job标注完成
        user = request.user
        for J_id in J_ids:
             #存储用户操作记录
            user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id))
            user_record.status=2 #not audited
            user_record.save()            

            
            job = Job.objects.get(id=J_id)
            job.status = 2
            job.save()
            segment = Segment.objects.get(id=job.segment_id)       
            segments = Segment.objects.filter(video_id = segment.video_id)      
            job_list = []       
            for seg in segments:
                job = Job.objects.get(segment_id = seg.id)
                job_list.append(job)
        
            for job in job_list:
                if job.status<2:#有segment还没有标完
                    return HttpResponse('success')
            
            video = Video.objects.get(id = segment.video_id)#该视频对应的seg全部标注完成
            video.status = 2
            video.save()            
        return HttpResponse('success')
    elif Action=='apply_audition':#申领视频
        user = request.user
        for J_id in J_ids:
            job = Job.objects.get(id=J_id)
            job.auditor_id = user.id  
            job.save()
            
            #保存用户操作记录            
            obj = User_Records(user_id=user.id,job_id=job.id)
            obj.save()
        return HttpResponse('success')
    elif Action=='apply_valuation':#申领视频
        user = request.user
        for J_id in J_ids:
            job = Job.objects.get(id=J_id)
            job.valuator_id = user.id  
            job.save()
            
            #保存用户操作记录   
            obj = User_Records(user_id=user.id,job_id=job.id)
            obj.save()
        return HttpResponse('success')
    elif Action=="valua_finish":
        user = request.user
        for J_id in J_ids:

            #存储用户操作记录
            user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id))
            user_record.status=1
            user_record.save()            

            job = Job.objects.get(id=J_id)
            job.status = 4
            job.save()
            segment = Segment.objects.get(id=job.segment_id)       
            segments = Segment.objects.filter(video_id = segment.video_id)      
            job_list = []       
            for seg in segments:
                job = Job.objects.get(segment_id = seg.id)
                job_list.append(job)
        
            for job in job_list:
                if job.status<4:#有segment还没有评价完
                    return HttpResponse('success')
            
            video = Video.objects.get(id = segment.video_id)#该视频对应的seg全部标注完成
            video.status = 4
            video.save()   
        return HttpResponse('success')
        
    elif Action=="appeal":
        user = request.user
        for J_id in J_ids:
            user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id))
            user_record.appeal = 2#修改状态为正在申诉，评价员可以看到，专门给重新判一下是否
            user_record.save()
        
             
    #job = Job.objects.get(id=J_id)
    #if job.istraining==0:#发布操作
     #   job.istraining = 1
    #if job.istraining==1:#申领操作
     #   job.istraining = 2
    #if job.istraining==2:#提交操作
     #   job.istraining = 3
    #if job.istraining==4:#提交操作
     #   job.istraining = 5
    #修改视频的状态，表示视频正在被操作
    #user = request.user
    #user_profile = Profile.objects.get(user_id=user.id)
    #user_profile.numsubmitted = user_profile.numsubmitted + 1
    #user_profile.save()
    
    #annotator_task_list(request)
    #generate_annotator_task()
    #return render(request,"video_tasks/annotator_task_list.html")
    return HttpResponseRedirect('/manage_job')
# job.id user.id operate:审议员接受获拒绝该视频标注


def access_appeal(request):
    J_ids = request.POST.getlist("J_id")
    user = request.user
    for J_id in J_ids:
        job = Job.objects.get(id=J_id)
        job.valuator_id = user.id  
        job.save()
            
        #保存用户操作记录   
        obj = User_Records(user_id=user.id,job_id=job.id)  
        obj.appeal=3     
        obj.save()

        segment = Segment.objects.get(id = job.segment_id)
        anno_id = Video.objects.get(id = segment.video_id).applied_id
        record = User_Records.objects.get(Q(user_id=anno_id),Q(job_id=J_id),Q(appeal=2))
        record.appeal = 3
        record.save()
    return HttpResponse('success')



@login_required 
def auditor_task(request):  
    user = request.user 
    J_ids = request.POST.getlist("J_id")
    operate = request.POST.get("operate")
    if operate=='y':
        #job被标记完成
        for J_id in J_ids:
            job = Job.objects.get(id=J_id)
            job.istraining = 4
            job.status = 3
            job.save()

            segment = Segment.objects.get(id=job.segment_id)       
            #存储用户操作记录
            anno_id = Video.objects.get(id = segment.video_id).applied_id
            user_record = User_Records.objects.get(Q(user_id=anno_id),Q(job_id=J_id))
            user_record.status=1
            user_record.save()
            
            #存储用户操作记录
            user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id))
            user_record.status=1
            user_record.save()  
            
            segments = Segment.objects.filter(video_id = segment.video_id)      
            job_list = []       
            for seg in segments:
                job = Job.objects.get(segment_id = seg.id)
                job_list.append(job)
        
            for job in job_list:
                if job.status<3:#有segment还没有标完
                    return HttpResponse('success')
            
            video = Video.objects.get(id = segment.video_id)#该视频对应的seg全部标注完成
            video.status = 3
            video.save()       
            #用户被接受视频数+1
            user = User.objects.get(id = video.applied_id)
            user_profile = Profile.objects.get(user_id=user.id)
            user_profile.numacceptances = user_profile.numacceptances + 1
    
        
    else:
        #job需要被重新标记
        for J_id in J_ids:
            job = Job.objects.get(id=J_id)
            job.istraining = 2
            job.status = 1 #状态恢复到未标注
            job.save()
            
            #用户被拒绝视频数+1
            segment = Segment.objects.get(id = job.segment_id)
            
            anno_id = Video.objects.get(id = segment.video_id).applied_id
            print(anno_id)
            print(J_id)
            user_record = User_Records.objects.get(Q(user_id=anno_id),job_id=J_id)
            if user_record!=None:
                user_record.status=0
                user_record.appeal = 1#标记为被拒之后可申诉
                user_record.save()
            
            #存储用户操作记录
            user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id))
            user_record.status=1
            user_record.save()              

            video = Video.objects.get(id = segment.video_id)       
            user = User.objects.get(id = video.applied_id)
            user_profile = Profile.objects.get(user_id=user.id)
            user_profile.numrejections = user_profile.numrejections + 1
            user_profile.save()
    #重新加载需要被审核的页面
    #generate_auditor_task()
    #return render(request,'video_tasks/auditor_task_list.html')
    return HttpResponse('success')


@login_required 
def handle_appeal(request):   
    user = request.user
    J_ids = request.POST.getlist("J_id")
    operate = request.POST.get("operate")
    print("hi handle_appeal")
    if operate=='y':
        #job被标记完成
        for J_id in J_ids:
            job = Job.objects.get(id=J_id)
            job.istraining = 4
            job.status = 3
            job.save()

            segment = Segment.objects.get(id=job.segment_id)       
            #存储用户操作记录
            anno_id = Video.objects.get(id = segment.video_id).applied_id
            user_record = User_Records.objects.get(Q(user_id=anno_id),Q(job_id=J_id))
            user_record.status=1 
            user_record.appeal = -1#已经申诉完成不可再申诉
            user_record.save()

            current_user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id),Q(appeal=3))
            current_user_record.status=1   
            current_user_record.appeal=-1      
            current_user_record.save()            
            



            segments = Segment.objects.filter(video_id = segment.video_id)      
            job_list = []       
            for seg in segments:
                job = Job.objects.get(segment_id = seg.id)
                job_list.append(job)
        
            for job in job_list:
                if job.status<3:#有segment还没有标完
                    return HttpResponse('success')
            
            video = Video.objects.get(id = segment.video_id)#该视频对应的seg全部标注完成
            video.status = 3
            video.save()       
            #用户被接受视频数+1
            user = User.objects.get(id = video.applied_id)
            user_profile = Profile.objects.get(user_id=user.id)
            user_profile.numacceptances = user_profile.numacceptances + 1
    
        
    else:
        #job需要被重新标记
        for J_id in J_ids:
            job = Job.objects.get(id=J_id)
            job.istraining = 2
            job.status = 1 #job状态恢复到未标注
            job.save()
            
            segment = Segment.objects.get(id=job.segment_id)#video状态恢复到未标注
            video = Video.objects.get(id = segment.video_id)
            video.status=1

             #用户被拒绝视频数+1
            segment = Segment.objects.get(id = job.segment_id)
            
            anno_id = Video.objects.get(id = segment.video_id).applied_id
            print(anno_id)
            print(J_id)
            user_record = User_Records.objects.get(Q(user_id=anno_id),job_id=J_id)           
            user_record.status=0
            user_record.appeal = -1#已经申诉完成不可再申诉
            user_record.save()
            
            current_user_record = User_Records.objects.get(Q(user_id=user.id),Q(job_id=J_id))
            current_user_record.status=1  
            current_user_record.appeal=-1            
            current_user_record.save() 

            
            video = Video.objects.get(id = segment.video_id)       
            user = User.objects.get(id = video.applied_id)
            user_profile = Profile.objects.get(user_id=user.id)
            user_profile.numrejections = user_profile.numrejections + 1
            user_profile.save()
    #重新加载需要被审核的页面
    #generate_auditor_task()
    #return render(request,'video_tasks/auditor_task_list.html')
    return HttpResponse('success')





#def valuator_task(request,level):    
    #跟用户等级有关？
    
def admin_welcome(request):
    return render(request,'video_tasks/index.html')

@login_required    
def manage_video(request):   
    return render(request,'video_tasks/manage_video.html')

@login_required 
def published_videos(request):
    videos = Video.objects.filter(Q(publish=1))
    paginator = Paginator(videos,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/published_videos.html',{'jobs':jobs})

@login_required 
def unpublished_videos(request):
    #videos = Video.objects.all()
    videos = Video.objects.filter(publish=0)
    paginator = Paginator(videos,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    return render(request,'video_tasks/unpublished_videos.html',{'jobs':jobs})

@login_required 
def manage_job(request):   
    videos = Video.objects.all()
    videos_new = [] 
    for video in videos:
        jobs_new = []
        segments = Segment.objects.filter(video_id = video.id) 
        for segment in segments:
            job = Job.objects.get(segment_id = segment.id)
            job_new = {"id":job.id,"length":segment.stop-segment.start,"status":job.status}
            jobs_new.append(job_new)
        video_new = {"id":video.id,"name":video.slug,"status":video.status,"jobs":jobs_new}
        videos_new.append(video_new)

    paginator = Paginator(videos_new,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    return render(request,'video_tasks/manage_job.html',{'videos':jobs})

@login_required 
def manage_data(request):   
    return render(request,'video_tasks/manage_data.html')

@login_required 
def finished_tasks(request):
    user = request.user
    print(user.profile.role)
    if user.profile.role=='Annoter':
        print("hi finish annotator")
        
        ## start new method to find the job_list finished by the annoter
        tasks = []
        user_records = User_Records.objects.filter(Q(user_id=user.id),Q(status=0)|Q(status=1)|Q(status=2))
        for user_record in user_records:
            job = Job.objects.get(id = user_record.job_id)
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":user_record.status}
            tasks.append(task)
        ## end
        
        paginator = Paginator(tasks,10)   
        page = request.GET.get('page',1)   
        currentpage = int(page)  
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    if user.profile.role=='Auditor':
        tasks = []
        user_records = User_Records.objects.filter(Q(user_id=user.id),Q(status=1))
        for user_record in user_records:
            job = Job.objects.get(id = user_record.job_id)
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":user_record.status}
            tasks.append(task)
                  
        paginator = Paginator(tasks,10)   
        page = request.GET.get('page',1)   
        currentpage = int(page)  
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    if user.profile.role=='Valuator':

        tasks = []
        user_records = User_Records.objects.filter(Q(user_id=user.id),Q(status=1))
        for user_record in user_records:
            job = Job.objects.get(id = user_record.job_id)
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":user_record.status}
            tasks.append(task)
        
        paginator = Paginator(tasks,10)   
        page = request.GET.get('page',1)   
        currentpage = int(page)  
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    return render(request,'video_tasks/finished_task_list.html',{'jobs':jobs})


def error_tasks(request):
    user = request.user
    print(user.profile.role)
    if user.profile.role=='Annoter':
        print("hi finish annotator")
        
        ## start new method to find the job_list finished by the annoter
        tasks = []
        user_records = User_Records.objects.filter(Q(user_id=user.id),Q(status=0))
        for user_record in user_records:
            job = Job.objects.get(id = user_record.job_id)
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":user_record.status}
            tasks.append(task)
        ## end
        
        paginator = Paginator(tasks,10)   
        page = request.GET.get('page',1)   
        currentpage = int(page)  
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    return render(request,'video_tasks/error_task_list.html',{'jobs':jobs})

def suc_tasks(request):
    user = request.user
    print(user.profile.role)
    if user.profile.role=='Annoter':
        print("hi finish annotator")
        
        ## start new method to find the job_list finished by the annoter
        tasks = []
        user_records = User_Records.objects.filter(Q(user_id=user.id),Q(status=1))
        for user_record in user_records:
            job = Job.objects.get(id = user_record.job_id)
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":user_record.status}
            tasks.append(task)
        ## end
        
        paginator = Paginator(tasks,10)   
        page = request.GET.get('page',1)   
        currentpage = int(page)  
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    return render(request,'video_tasks/suc_task_list.html',{'jobs':jobs})


    
@login_required 
def searchvideos(request,action,content):
    #需要知道身份还有就是干什么
    print(action)
    print(content)
    user = request.user
    role = Profile.objects.get(user_id=user.id).role
    #role = user.profile.role
    if role == 'admin':
        if action == 'publish':
            tasks = Video.objects.filter(Q(publish=1),Q(slug=content))
        else:
            tasks = Video.objects.filter(Q(publish=0),Q(slug=content))
    elif role == 'Annoter':
        if action == 'apply':
            tasks = Video.objects.filter(Q(publish=1),Q(applied_id=-1),Q(slug=content))#已发布且未被申领的视频
        elif action == 'doing':
            video_list = Video.objects.filter(Q(applied_id = user.id),Q(status=1),Q(slug=content))#被当前标注员申领过的视频
            segment_list = []
            for video in video_list:
                segments = Segment.objects.filter(video_id = video.id)
                for segment in segments:
                    segment_list.append(segment)
            job_list=[]
            for segment in segment_list:
                print(segment.id)
                try:
                    job = Job.objects.get(Q(segment_id=segment.id)&Q(status=1))
                    job_list.append(job)
                except:
                    pass
        
            tasks = []
            for job in job_list:       
                segment = Segment.objects.get(id=job.segment_id)            
                video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
                print(video.id)
                task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start}
                tasks.append(task)
        else:
            video_list = Video.objects.filter(Q(applied_id = user.id),Q(status=1)|Q(status=2)|Q(status=3)|Q(status=4),Q(slug=content))#被当前标注员申领过的视频
            segment_list = []
            for video in video_list:
                segments = Segment.objects.filter(video_id = video.id)
                for segment in segments:
                    segment_list.append(segment)
            job_list=[]
            for segment in segment_list:
                try:
                    job = Job.objects.get(Q(segment_id=segment.id),Q(status=2)|Q(status=3)|Q(status=4))
                    job_list.append(job)
                except:
                     pass
            tasks = []
            for job in job_list:
                segment = Segment.objects.get(id=job.segment_id)
                video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
                print(video.id)
                task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
                tasks.append(task)
    elif role == 'Auditor':
        if action == 'apply':
            job_list = Job.objects.filter(Q(status = 2),Q(auditor_id=-1),Q(id=content))            
        elif action == 'doing':           
            job_list = Job.objects.filter(Q(auditor_id = user.id),Q(status=2),Q(id=content))
        else:
            job_list = Job.objects.filter(Q(auditor_id = user.id),Q(status=3)|Q(status=4),Q(id=content))                 
        tasks = []
        for job in job_list:
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            print(video.id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
            tasks.append(task)
    else:
        if action == 'apply':
            job_list = Job.objects.filter(Q(status = 3),Q(valuator_id=-1),Q(id=content))
            
        elif action == 'doing':
            job_list = Job.objects.filter(Q(valuator_id = user.id)&Q(status=3),Q(id=content))
            
        else:
            job_list = Job.objects.filter(Q(valuator_id = user.id),Q(status=4),Q(id=content))#被当前标注员申领过的视频 
            
        tasks = []
        for job in job_list:
            segment = Segment.objects.get(id=job.segment_id)
            video = Video.objects.get(id = Segment.objects.get(id=job.segment_id).video_id)
            print(video.id)
            task = {"job_id":job.id,"video_slug":video.slug,"segment_length":segment.stop-segment.start,"status":job.status}
            tasks.append(task)
    
        
    paginator = Paginator(tasks,10)   
    page = request.GET.get('page',1)   
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    
    
    if role == 'admin':
        if action == 'publish':
            return render(request,'video_tasks/published_videos.html',{'jobs':jobs})
        else:
            return render(request,'video_tasks/unpublished_videos.html',{'jobs':jobs})
    else:
        if action == 'apply':
            if role =='Annoter':
                return render(request,'video_tasks/apply_annotation_tasks.html',{'jobs':jobs})
            else:
                return render(request,'video_tasks/apply_tasks.html',{'jobs':jobs})
        elif action == 'finished':
            return render(request,'video_tasks/finished_task_list.html',{'jobs':jobs})       
        else:
            if role =='Annoter':
                return render(request,'video_tasks/annotator_task_list.html',{'jobs':jobs})
            elif role == 'Auditor':
                return render(request,'video_tasks/auditor_task_list.html',{'jobs':jobs})
            else:
                return render(request,'video_tasks/valuator_task_list.html',{'jobs':jobs})

def web_index(request):
    return render(request,'userApp/va_web.html')


 
def testindex(request):
    videos = Video.objects.all()#video
    video_num = videos.count()#the num of videos
    job_num = Job.objects.all().count()#the num of jobs 
    video_frame_num = 0
    for video in videos:
       video_frame_num = video_frame_num+video.totalframes#the num of frames
    print(video_frame_num)
    box_num = Box.objects.filter(outside=0).count()#the num of boxes

    return render(request,'userApp/index.html',{'video_num':video_num,'job_num':job_num})   
    #return render(request,'userApp/index_new.html')   

#测试代码
def testpage(request):
    job_list = Job.objects.all()
    segments = Segment.objects.all()
    videos = Video.objects.all()
    paginator = Paginator(job_list,10)   
    page = request.GET.get('page',1) #取页数 没取到默认为第一页  
    currentpage = int(page)  
    try:
            jobs = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
    return render(request,'video_tasks/page_test.html',{'jobs':jobs,'segments':segments,'videos':videos})

def changejobstatus_group(request,Action,J_idlist):
    #为发布状态 0  
    #发布状态 1
    #申领状态 2
    #提交状态 3
    #1审核通过4
    #1审核不通过2
    #2审核结果提交 5
    if Action=='publish':#发布状态修改成功
        videolist=[]
        for id in J_idlist:
            video = Video.objects.get(id=J_id)
            video.publish = 1
            video.status = 1
            videolist.append(video)
            video.save()
        segments=[]    
        for video in videolist:
            segment = Segment.objects.filter(video_id = video.id)
            segments.append(segment)
        for seg in segments:
            job = Job.objects.get(segment_id = seg.id)
            job.status = 1
            job.save()
        print(J_id)
        print("publish change status")        
        return HttpResponseRedirect('/unpublished_videos')  
    elif Action=='unpublish':
        video = Video.objects.get(id=J_id)
        video.publish = 0
        print(J_id)
        print("unpublish change status")
        video.save()  
        return HttpResponseRedirect('/published_videos')  
    
    elif Action=='apply':#申领视频
        user = request.user
        video = Video.objects.get(id=J_id)
        video.applied_id = user.id
        video.save()
        return HttpResponseRedirect('/applytasklist')
    elif Action=='anno_finish':#job标注完成
        user = request.user
        job = Job.objects.get(id=J_id)
        job.status = 2
        job.save()
        segment = Segment.objects.get(id=job.segment_id)       
        segments = Segment.objects.filter(video_id = segment.video_id)      
        job_list = []       
        for seg in segments:
            job = Job.objects.get(segment_id = seg.id)
            job_list.append(job)
        
        for job in job_list:
            if job.status<2:#有segment还没有标完
                return HttpResponseRedirect('/annotertasklist')
            
        video = Video.objects.get(id = segment.video_id)#该视频对应的seg全部标注完成
        video.status = 2
        video.save()            
        return HttpResponseRedirect('/annotertasklist')
    elif Action=='apply_audition':#申领视频
        user = request.user
        job = Job.objects.get(id=J_id)
        job.auditor_id = user.id  
        job.save()
        return HttpResponseRedirect('/apply_tasks')
    elif Action=='apply_valuation':#申领视频
        user = request.user
        job = Job.objects.get(id=J_id)
        job.valuator_id = user.id  
        job.save()
        return HttpResponseRedirect('/apply_tasks')
    elif Action=="valua_finish":
        user = request.user
        job = Job.objects.get(id=J_id)
        job.status = 4
        job.save()
        segment = Segment.objects.get(id=job.segment_id)       
        segments = Segment.objects.filter(video_id = segment.video_id)      
        job_list = []       
        for seg in segments:
            job = Job.objects.get(segment_id = seg.id)
            job_list.append(job)
        
        for job in job_list:
            if job.status<4:#有segment还没有评价完
                return HttpResponseRedirect('/annotertasklist')
            
        video = Video.objects.get(id = segment.video_id)#该视频对应的seg全部标注完成
        video.status = 4
        video.save()   
        return HttpResponseRedirect('/valuatortasklist')
    
    
    
                 
    return HttpResponseRedirect('/manage_job')

def introduction(request):
    return render(request,'video_tasks/introduction.html')

def testforlink(request):
     return render(request,'video_tasks/testforlink.html')


def test(request):
    os.system('ssh root@10.10.10.35')
    return ('success')

def img_eval(self):
    #jarpath = os.path.join(os.path.abspath('.'),'/home/olivia/Desktop/handin/')
    #print(jarpath)
    #jpype.startJVM(jpype.getDefaultJVMPath(),"-Djava.ext.dirs=%s" % jarpath)
    #javaClass = jpype.JClass('ui.HelloLabel')
    #javaInstance = javaClass.main()
    #jpype.java.lang.System.out.println("hello world!") 
    #jpype.shutdownJVM()
    os.system('java -jar /home/olivia/Desktop/handin/imageEstimate.jar')
    return HttpResponseRedirect('/dumptasklist')

