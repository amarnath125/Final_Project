# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid

# Create your models here.
class UserModel(models.Model):
    email      = models.EmailField()
    name       = models.CharField(max_length=120)
    username   = models.CharField(max_length=120)
    password   = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


#session tracking
class SessionToken(models.Model):
    user          = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on    = models.DateTimeField(auto_now_add=True)
    is_valid      = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()
        

#post
class PostModel(models.Model):
    user       = models.ForeignKey(UserModel)
    image      = models.FileField(upload_to='user_images')
    image_url  = models.CharField(max_length=255)
    caption    = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


""" 
#just checking data from tabel UserModel

get=UserModel.objects.all()
lget=len(get)
x=1
while x<=lget:
    get = UserModel.objects.get(id=x)
    print get.username
    x+=1
"""

