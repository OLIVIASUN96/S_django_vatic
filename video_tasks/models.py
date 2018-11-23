# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import CITIS.database
import random
import logging
import video_tasks.config
from CITIS.models import *
#from CITIS.models import HIT,BonusSchedule
from sqlalchemy import Column, Integer, Float, String, Boolean, Text
from sqlalchemy import ForeignKey, Table, PickleType
from sqlalchemy.orm import relationship, backref
import pyvision.vision
from sqlalchemy.sql.elements import Null


boxes_attributes = Table("boxes2attributes", CITIS.database.Base.metadata,
    Column("box_id", Integer, ForeignKey("boxes.id")),
    Column("attribute_id", Integer, ForeignKey("attributes.id")))

# Create your models here.
#视频
class Video(models.Model):
    slug = models.CharField(max_length=250,null=True)
    description = models.CharField(max_length=250,null=True)#视频描述字段
    uploaderid = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    totalframes = models.IntegerField(null=True)
    location = models.CharField(max_length=250,null=True)
    skip = models.IntegerField(default = 0)
    perobjectbonus = models.FloatField(default = 0,null=True)
    completionbonus = models.FloatField(default = 0,null=True)
    isfortraining = models.SmallIntegerField(default = 0,null=True)
    trainvalidator = models.TextField(blank=True,null=True)
    blowradius = models.IntegerField(default = 0,null=True)
    scene = models.CharField(max_length = 50,null=True)
    resolutionx = models.IntegerField(null=True)
    resolutiony = models.IntegerField(null=True)
    videoannodocument = models.CharField(max_length=250,null=True)
    type = models.CharField(max_length=40,null=True)
    publish = models.IntegerField(default=0)
    applied_id = models.IntegerField(default=-1)
    auditor_id = models.IntegerField(default=-1)
    valuator_id = models.IntegerField(default=-1)
    status = models.IntegerField(default=0)
    class Meta:
        db_table = 'videos'
        app_label = 'video_tasks'

    def __getitem__(self, frame):
        path = Video.getframepath(frame, self.location)
        return Image.open(path)

    @classmethod
    def getframepath(cls, frame, base = None):
        l1 = frame // 10000
        l2 = frame // 100
        path = "{0}/{1}/{2}.jpg".format(l1, l2, frame)
        if base is not None:
            path = "{0}/{1}".format(base, path)
        return path

    @property
    def cost(self):
        cost = 0
        for segment in self.segments:
            cost += segment.cost
        return cost

    @property
    def numjobs(self):
        count = 0
        for segment in self.segments:
            for job in segment.jobs:
                count += 1
        return count

    @property
    def numcompleted(self):
        count = 0
        for segment in self.segments:
            for job in segment.jobs:
                if job.completed:
                    count += 1
        return count

#标签
class Label(models.Model):
     __tablename__ = "labels"

     class Meta:
        db_table = 'labels'
        app_label = 'video_tasks'

     text = models.CharField(max_length=250,null=True)
     #video = models.OneToOneField(Video,on_delete=models.CASCADE)
     video = models.ForeignKey(Video,related_name = 'video_label',on_delete=models.CASCADE)

#标签属性
class Attribute(models.Model):
    __tablename__ = "attributes"

    class Meta:
        db_table = 'attributes'
        app_label = 'video_tasks'

    text = models.CharField(max_length=250,null=True)
    #label = models.OneToOneField(Label,on_delete=models.CASCADE)
    label = models.ForeignKey(Label,related_name = 'label_attribute',on_delete=models.CASCADE)
    def __str__(self):
        return self.text

#视频片段
class Segment(models.Model):
    __tablename__ = "segments"

    #videoid = models.OneToOneField(Video,on_delete=models.CASCADE) 这个好像
    video = models.ForeignKey(Video,related_name = 'segments_video',on_delete=models.CASCADE)
    start = models.IntegerField(null=True)
    stop = models.IntegerField(null=True)

    class Meta:
        db_table = 'segments'
        app_label = 'video_tasks'

    @property
    def paths(self):
        paths = []
        for job in self.jobs:
            if job.useful:
                paths.extend(job.paths)
        return paths

    @property
    def cost(self):
        cost = 0
        for job in self.jobs:
            cost += job.cost
        return cost

#任务
class Job(models.Model):
    __tablename__ = "jobs"
   
    segment = models.OneToOneField(Segment,on_delete=models.CASCADE)
    istraining = models.SmallIntegerField(default = 0,null=True)
    status = models.IntegerField(default = 0)
    auditor_id = models.IntegerField(default = -1)
    valuator_id = models.IntegerField(default = -1)
    evaluate = models.IntegerField(default = -1)
    
    class Meta:
        db_table = 'jobs'
        app_label = 'video_tasks'

    def getpage(self):
        return "?id={0}".format(self.id)

    def markastraining(self):
        """
        Marks this job as the result of a training run. This will automatically
        swap this job over to the training video and produce a replacement.
        """
        replacement = Job(segment = self.segment, group = self.group)
        self.segment = self.segment.video.trainwith.segments[0]
        self.group = self.segment.jobs[0].group
        self.istraining = True

        logger.debug("Job is now training and replacement built")

        return replacement

    def invalidate(self):
        """
        Invalidates this path because it is poor work. The new job will be
        respawned automatically for different workers to complete.
        """
        self.useful = False
        # is this a training task? if yes, we don't want to respawn
        if not self.istraining:
            return Job(segment = self.segment, group = self.group)


    @property
    def trainingjob(self):
        return self.segment.video.trainwith.segments[0].jobs[0]

    @property
    def validator(self):
        return self.segment.video.trainvalidator

    @property
    def cost(self): 
        if not self.completed:
            return 0
        return self.bonusamount + self.group.cost + self.donatedamount

    def __iter__(self):
        return self.paths

#Path
class Path(models.Model):
    __tablename__ = "paths"
    
    job = models.ForeignKey(Job,related_name='path_job',default=None,on_delete=models.CASCADE)  
    label = models.ForeignKey(Label,related_name='path_label',default=None,on_delete=models.CASCADE) 
    interpolatecache = None


    class Meta:
        db_table = 'paths'
        app_label = 'video_tasks'

    def getboxes(self, interpolate = False, bind = False, label = False):
        #result = [x.getbox() for x in self.boxes] #可以通过pathid 得到对应的boxes
        print('self.id')
        print(self.id)
        #result = [x.getbox() for x in Box.objects.filter(pathid_id = self.id)]
        result = [x.getbox() for x in Box.objects.filter(pathid_id = self.id)]
        #for box in result:
           # print(box.id)
            #print(box.xtl)
            #print(box.ytl)
           # print(box.xbr)
            #print(box.ybr)
            #print(box.frame)
            #print(box.pathid_id)
            
        #result.sort(key = lambda x: x.frame)
        result.sort(key = lambda x: x[4])
        if interpolate:
            if not self.interpolatecache:
                self.interpolatecache = LinearFill(result)
            result = self.interpolatecache

        if bind:
            result = Path.bindattributes(self.attributes, result)

        if label:
            for box in result:
                box.attributes.insert(0, self.label.text)
        
        return result

    @classmethod 
    def bindattributes(cls, attributes, boxes):
        attributes = sorted(attributes, key = lambda x: x.frame)

        byid = {}
        for attribute in attributes:
            if attribute.attributeid not in byid:
                byid[attribute.attributeid] = []
            byid[attribute.attributeid].append(attribute)

        for attributes in byid.values():
            for prev, cur in zip(attributes, attributes[1:]):
                if prev.value:
                    for box in boxes:
                        if prev.frame <= box.frame < cur.frame:
                            if prev.attribute not in box.attributes:
                                box.attributes.append(prev.attribute)
            last = attributes[-1]
            if last.value:
                for box in boxes:
                    if last.frame <= box.frame:
                        if last.attribute not in box.attributes:
                            box.attributes.append(last.attribute)

        return boxes

    def __repr__(self):
        return "<Path {0}>".format(self.id)

class AttributeAnnotation(models.Model):
    __tablename__ = "attribute_annotations"

    path = models.ForeignKey(Path,related_name = 'AttrAnno_Path',default=-1,on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute,related_name='AttrAnno_Attr',default=-1,on_delete=models.CASCADE)
    frame = models.IntegerField()
    value = models.SmallIntegerField(default = False)

    class Meta:
        db_table = 'attribute_annotations'
        app_label = 'video_tasks'

    def __repr__(self):
        return ("AttributeAnnotation(pathid = {0}, "
                                    "attributeid = {1}, "
                                    "frame = {2}, "
                                    "value = {3})").format(self.pathid,
                                                           self.attributeid,
                                                           self.frame,
                                                           self.value)




#boxes
class Box(models.Model):
    __tablename__ = "boxes"

    #pathid = models.OneToOneField(Path,on_delete=models.CASCADE)  
    pathid = models.ForeignKey(Path,related_name = 'box_path',on_delete=models.CASCADE)
    xtl = models.IntegerField()
    ytl = models.IntegerField()
    xbr = models.IntegerField()
    ybr = models.IntegerField()
    frame = models.IntegerField()
    occluded = models.SmallIntegerField(default = False)
    outside = models.SmallIntegerField(default = False)
    isrevised = models.SmallIntegerField(default = False)
   
    class Meta:
        db_table = 'boxes'
        app_label = 'video_tasks'

    def getbox(self):
        #return vision.Box(self.xtl, self.ytl, self.xbr, self.ybr,
                          #self.frame, self.outside, self.occluded, 0)
        
        #return Box(self.xtl, self.ytl, self.xbr, self.ybr,
                          #self.frame, self.outside, self.occluded, 0)
        
        return (self.xtl, self.ytl, self.xbr, self.ybr,
                          self.frame, self.outside, self.occluded, None, None, 0, 0.0, [])


class User_Records(models.Model):
    __tablename__ = "user_records"
   
    user = models.ForeignKey(User,related_name='user_records',on_delete=models.CASCADE)
    job = models.ForeignKey(Job,related_name='job_user_records',on_delete=models.CASCADE)
    status = models.IntegerField(default = -1)  
    appeal = models.IntegerField(default = 0)
    
    class Meta:
        db_table = 'user_records'
        app_label = 'video_tasks'


# #user expansion
# class UserProfile(models.Model):
#     user = models.OneToOneField(User)    
#     major = models.TextField(default='', blank=True)
#     address = models.CharField(max_length=200,default='',blank=True)

#     def __unicode__(self):
#         return self.user.username

#     def create_user_profile(sender, instance, created, **kwargs):
#         """Create the UserProfile when a new User is saved"""
#         if created:
#             profile = UserProfile()
#             profile.user = instance
#             profile.save()


# #user expansion
