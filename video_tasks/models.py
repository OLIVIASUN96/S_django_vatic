# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User)

    def __str__(self):
        return self.text


class Entry(models.Model):
    task=models.ForeignKey(Task)
    text=models.TextField()
    date_added=models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural='entries'

    def __str__(self):
        if (len(self.text)>=50):
            return self.text[:50]+"..."
        return self.text


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