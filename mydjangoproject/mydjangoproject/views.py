# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#from datetime import datetime
from demoapp.forms import SignUpForm
from django.contrib.auth.hashers import make_password   # to encrypt the pswrd
from demoapp.models import UserModel

# Create your views here.
def signup_view(request):
    if request.method == 'GET':
        #display signup form
        signup_form = SignUpForm()
    
    elif request.method == 'POST': 
        #process the form data
        signup_form = SignUpForm(request.POST)
        
        #validate the form data
        if signup_form.is_valid():
            #validation sucessfull
            username = signup_form.cleaned_data['username']
            name     = signup_form.cleaned_data['name']
            email    = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            
            #save data to db
            new_user = UserModel(name = name, email = email,password = make_password(password), username = username)
            new_user.save()    

    return render(request,'signup.html',{'signup_form':signup_form})
