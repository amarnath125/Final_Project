# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
from demoapp.forms import SignUpForm

# Create your views here.
def signup_view(request):
    today = datetime.now
    signup_form = SignUpForm()
    return render(request,'signup.html',{'signup_form':signup_form})
    

