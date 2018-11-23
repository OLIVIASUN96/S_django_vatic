 # -*- coding: UTF-8 -*-

from django.db import models
from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy import ForeignKey, Index, DateTime, Numeric
from sqlalchemy.orm import relationship, backref
import CITIS.database
import CITIS.api
import random
import logging
import math
import CITIS.geolocation

logger = logging.getLogger("CITIS.models")

"""
class Enum(set):
    ###定义enum类型
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
"""


class HITGroup(models.Model):
    __tablename__ = "CITIS_hit_groups"

    title = models.CharField(max_length=250,null=False)
    description = models.CharField(max_length=250,null=False)
    duration = models.IntegerField(null=False)
    lifetime = models.IntegerField(null=False)
    cost = models.FloatField(null=False) 
    keywords = models.CharField(max_length=250,null=False)
    height = models.IntegerField(null=False,default = 650)
    donation = models.IntegerField(null=True,default = 0)  # 0=off,
    # 1=option,
    # 2=force
    offline =  models.SmallIntegerField(null=True,default = False)
    minapprovedamount = models.IntegerField(null=True,default=None)
    minapprovedpercent = models.IntegerField(null=True,default=None)
    countrycode = models.CharField(null=True,max_length=10,default=None)

    class Meta:
        db_table = 'CITIS_hit_groups'
        app_label = 'CITIS'

class Worker(models.Model):
    __tablename__ = "CITIS_users"

    username = models.CharField(max_length=40,null=False)
    password = models.CharField(max_length=40,null=False)
    type = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=40,null=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    numaccount = models.IntegerField()
    phonenum = models.IntegerField()
    workexper = models.TextField()
    educationback = models.TextField()
    userlevel = models.IntegerField()
    numuploaded = models.IntegerField()
    numsubmitted = models.IntegerField(default=0,null=False)
    numacceptances = models.IntegerField(default=0,null=False)
    numrejections = models.IntegerField(default=0,null=False)
    blocked =  models.SmallIntegerField(default = False)
    donatedamount = models.FloatField(default=0.0,null=False) 
    bonusamount = models.FloatField(default=0.0,null=False) 
    verified =  models.SmallIntegerField(default = False)
 

    class Meta:
        db_table = 'CITIS_users'
        app_label = 'CITIS'


    def block(self, reason):
        api.server.block(self.id, reason)
        self.blocked = True

    def unblock(self, reason):
        api.server.unblock(self.id, reason)
        self.blocked = False

    def email(self, subject, message):
        api.server.email(self.id, subject, message)

    @classmethod
    def lookup(self, workerid, session=None):
        if not session:
            session = CITIS.database.session

        worker = session.query(Worker)
        worker = worker.filter(Worker.id == workerid)

        if worker.count() > 0:
            worker = worker.one()
            logger.debug("Found existing worker {0}".format(workerid))
        else:
            worker = Worker(
                id=workerid,
                numsubmitted=0,
                numacceptances=0,
                numrejections=0)
            logger.debug("Created new worker {0}".format(workerid))
        return worker

    @property
    def ips(self):
        return set(x.ipaddress for x in self.tasks)

    @property
    def locations(self):
        locs = [CITIS.geolocation.lookup(x) for x in self.ips]
        return [x for x in locs if x]

    #登陆
    def login(self, _username, _password, _type):
        session = CITIS.database.session

        worker = session.query(Worker)
        worker = worker.filter((Worker.username == _username) & (Worker.password == _password) & (Worker.type == _type))

        if worker.count() > 0:
            worker = worker.one()
            logger.debug("Found existing worker {0}".format(_username))
        else:
            raise RuntimeError("user doesn't exist or password isn't correct or usertype isn't correct")
            logger.debug("login failed".format(_username))
        return worker

    #注册
    def register(self,_username,_password,_type,_address,_email,_age,_gender,_numaccount,_workexper,_educationback,_phonenum):
        session = CITIS.database.session
        worker = Worker(
            username=_username,
            password =_password,
            type = _type,
            address = _address,
            email = _email,
            age = _age,
            gender = _gender,
            numaccount = _numaccount,
            phonenum = _phonenum,
            workexper = _workexper,
            educationback = _educationback,
            userlevel = 1,
            numuploaded = 0,
            numsubmitted = 0,
            numacceptances = 0,
            numrejections = 0,
            blocked = 0,
            donatedamount = 0.0,
            bonusamount = 0,
            verified = 0)
        logger.debug("Created new worker {0}".format(workerid))
        session.add(worker)
        session.commit()

        return worker

class HIT(models.Model):
    __tablename__ = "CITIS_hits"

    hitslug = models.CharField(max_length=30,null=True)
    #group = models.OneToOneField(HITGroup,on_delete=models.CASCADE)
    #video = models.ForeignKey(Video,related_name = 'segments_video')
    group = models.ForeignKey(HITGroup,related_name = 'hitgroup_hit',on_delete='models.CASCADE')
    description = models.TextField(null=True)
    depth =  models.FloatField(null=True)

    worker_id = models.IntegerField(null = True)
    #worker_id = models.OneToOneField(Worker,on_delete=models.CASCADE,related_name='workhits')
    # worker        = relationship(Worker, backref="hits")
 
    checker_id = models.IntegerField(null = True)
    #checker_id = models.OneToOneField(Worker,on_delete=models.CASCADE,related_name='checkhits')
    # checker       = relationship(Worker, backref = "hits")

    ready =  models.SmallIntegerField(default = True,null=True)
    published =  models.SmallIntegerField(default = False,null=True)
    completed =  models.SmallIntegerField(default = False,null=True)
    compensated =  models.SmallIntegerField(default = False,null=True)
    checked =  models.SmallIntegerField(default = False,null=True)
    accepted =  models.SmallIntegerField(default = False,null=True)
    validated =  models.SmallIntegerField(default = False,null=True)
    reason = models.TextField(null=True)
    isdisputed =  models.SmallIntegerField(default = False,null=True)
    disputedcontent = models.TextField(null=True)

    commenter_id = models.IntegerField(null = True)
    #commenter_id = models.OneToOneField(Worker,on_delete=models.CASCADE,related_name='commandhits')
    # commenter     = relationship(Worker,backref = "hits")
    comments = models.TextField(null=True)
    timeaccepted = models.DateTimeField(null=True)
    timecompleted = models.DateTimeField(null=True)
    timeonserver = models.DateTimeField(null=True)
    ipaddress = models.CharField(max_length=15,null=True) 
    page = models.CharField(max_length=250,null=False,default=" ")
    completeness = models.FloatField(null=True)
    quality = models.FloatField(null=True)
    donatedamount = models.FloatField(default=0.0,null=False)
    bonusamount = models.FloatField(default=0.0,null=False)
    useful = models.SmallIntegerField(default = True,null=True)
    annodocument =  models.CharField(max_length=250,null=True) 

    type = models.CharField(max_length=250) 

    class Meta:
        db_table = 'CITIS_hits'
        app_label = 'CITIS'

    def publish(self):
        if self.published:
            raise RuntimeError("HIT cannot be published because it has already"
                               " been published.")
        resp = api.server.createhit(
            title=self.group.title,
            description=self.group.description,
            amount=self.group.cost,
            duration=self.group.duration,
            lifetime=self.group.lifetime,
            keywords=self.group.keywords,
            height=self.group.height,
            minapprovedamount=self.group.minapprovedamount,
            minapprovedpercent=self.group.minapprovedpercent,
            countrycode=self.group.countrycode,
            page=self.getpage())
        self.hitid = resp.hitid
        self.published = True
        logger.debug("Published HIT {0}".format(self.hitid))

    def getpage(self):
        raise NotImplementedError()

    def markcompleted(self, workerid):
        try:
            workerid.numsubmitted
        except:
            session = CITIS.database.Session.object_session(self)
            worker = Worker.lookup(workerid, session)
        else:
            worker = workerid

        self.completed = True
        self.worker = worker
        self.worker.numsubmitted += 1

        logger.debug("HIT {0} marked complete".format(self.hitid))

    def disable(self):
        if not self.published:
            raise RuntimeError("HIT cannot be disabled because "
                               "it is not published")
        if self.completed:
            raise RuntimeError("HIT cannot be disabled because "
                               "it is completed")
        api.server.disable(self.hitid)
        oldhitid = self.hitid
        self.published = False
        self.hitid = None
        logger.debug("HIT (was {0}) disabled".format(oldhitid))
        return oldhitid

    def accept(self, reason=None, bs=True):
        if not reason:
            if bs:
                reason = random.choice(reasons)
            else:
                reason = ""

        for schedule in self.group.schedules:
            schedule.award(self)

        if self.donatedamount > 0:
            reason = (reason + " For this HIT, we have donated ${0:>4.2f} to "
                               "the World Food Programme on your behalf. Thank you for your "
                               "support!".format(self.donatedamount))

        api.server.accept(self.assignmentid, reason)
        self.accepted = True
        self.compensated = True
        self.worker.numacceptances += 1

        logger.debug("Accepted work for HIT {0}".format(self.hitid))

    def warn(self, reason=None):
        if not reason:
            reason = ("Warning: we will start REJECTING your work soon if you"
                      "do not improve your quality. Please reread the instructions.")
        api.server.accept(self.assignmentid, reason)
        self.accepted = True
        self.compensated = True
        self.worker.numacceptances += 1

        logger.debug("Accepted, but warned for HIT {0}".format(self.hitid))

    def reject(self, reason=""):
        try:
            api.server.reject(self.assignmentid, reason)
        except:
            print
            "Failed to reject {0}".format(self.assignmentid)
        self.accepted = False
        self.compensated = True
        self.worker.numrejections += 1

        logger.debug("Rejected work for HIT {0}".format(self.hitid))
    
   

   
    def awardbonus(self, amount, reason=None, bs=True):
        self.donatedamount += amount * self.opt2donate
        self.worker.donatedamount += amount * self.opt2donate

        amount = math.floor(amount * (1 - self.opt2donate) * 100) / 100

        if amount > 0:
            logger.debug("Awarding bonus of {0} on HIT {1}"
                         .format(amount, self.hitid))
            self.bonusamount += amount
            self.worker.bonusamount += amount
            if not reason:
                if bs:
                    reason = random.choice(reasons)
                else:
                    reason = ""
            api.server.bonus(self.workerid, self.assignmentid, amount, reason)

    def offlineurl(self, localhost):
        return "{0}{1}&hitId=offline".format(localhost, self.getpage())

    def invalidate(self):
        raise NotImplementedError("Subclass must implement 'invalid()'")


class EventLog(models.Model):
    __tablename__ = "CITIS_event_log"

    hitid =  models.OneToOneField(HIT,on_delete=models.CASCADE)
    domain = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'CITIS_event_log'
        app_label = 'CITIS'

class BonusSchedule(models.Model):
    __tablename__ = "CITIS_bonus_schedules"

    groupid =  models.OneToOneField(HITGroup,on_delete=models.CASCADE)
    discriminator = models.CharField(max_length=250) 

    class Meta:
        db_table = 'CITIS_bonus_schedules'
        app_label = 'CITIS'

    def award(self, hit):
        raise NotImplementedError()

    def description(self):
        raise NotImplementedError()


class ConstantBonus(BonusSchedule):
    __tablename__ = "CITIS_bonus_schedule_constant"
    __maper_args__ = {"polymorphic_identity": "CITIS_constant"}

    bid =  models.OneToOneField(BonusSchedule,on_delete=models.CASCADE,primary_key=True)
    amount = models.FloatField(null=False)

    class Meta:
        db_table = 'CITIS_bonus_schedule_constant'
        app_label = 'CITIS'

    def award(self, hit):
        hit.awardbonus(self.amount, "For completing the task.")
        return self.amount

    def description(self):
        return (self.amount, "bonus")



reasons = [""]
# reasons = ["Thanks for your hard work!",
#           "Excellent work!",
#           "Excellent job!",
#           "Great work!",
#           "Great job!",
#           "Fantastic job!",
#           "Perfect!",
#           "Thank you!",
#           "Please keep working!",
#           "Your work is helping advance research.",
#           "We appreciate your work.",
#           "Please keep working.",
#           "You are doing an excellent job.",
#           "You are doing a great job.",
#           "You are doing a superb job.",
#           "Keep up the fantastic work!"]
