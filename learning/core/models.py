from django.db import models

#Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#auth_user的其他配置
class Profile(models.Model):
    ANNOTER = 'Annoter'#1
    AUDITOR = 'Auditor'#2
    VALUATOR = 'Valuator'#3
    ROLE_CHOICES = (
        (ANNOTER, 'Annoter'),
        (AUDITOR, 'Auditor'),
        (VALUATOR, 'Valuator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, null=True, blank=True, max_length=10)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    phone=models.CharField(max_length=15,blank=True)
    STUDENT = 'student'#1
    WORKER = 'worker'#2
    OTHER = 'other'#3
    EDUBACK_CHOICES = (
        (STUDENT, 'student'),
        (WORKER, 'worker'),
        (OTHER, 'other'),
    )
    edubackground = models.CharField(choices=EDUBACK_CHOICES,max_length=30,blank=True)
    sex = models.CharField(max_length=15,blank=True)
    
    bankaccount = models.CharField(u'银行卡号',null=True,max_length=40)
    workexper = models.TextField(blank=True)
    userlevel = models.IntegerField(u'用户等级1,2,3...',null=True)
    numuploaded = models.IntegerField(u'上传视频数量',null=True,default=0) 
    numsubmitted = models.IntegerField(u'已完成数量',default=0) 
    numacceptances = models.IntegerField(u'被接收数量',default=0)
    numrejections = models.IntegerField(u'被拒绝数量',default=0)
    blocked = models.IntegerField(u'是否被锁定',default=0)
    bonusamount = models.FloatField(u'薪酬总计',default=0) 
    verified = models.IntegerField(u'是否被认证',default=0) 
    donatedamount = models.FloatField(u'捐助数额',default=0) 
    
    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def __str__(self):
        return self.user.username


#@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
    #if created:
        #Profile.objects.create(user=instance)
    #instance.profile.save()