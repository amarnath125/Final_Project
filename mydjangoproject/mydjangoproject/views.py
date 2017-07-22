# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from demoapp.forms import SignUpForm,LoginForm
from django.contrib.auth.hashers import make_password,check_password   # make_password is used to encrypt the pswrd
from demoapp.models import UserModel,SessionToken


# Create your views here.
def feed_view(request):
    if request.method == 'GET':
        return render(request,'feed.html')


def signup_view(request):
    if request.method == 'GET':
        signup_form = SignUpForm()                             # calling & display signup form
        template_name = 'signup.html'                          # rendering to signup.html after get reqst

    elif request.method == 'POST':
        signup_form = SignUpForm(request.POST)                 # calling & process the form data
        if signup_form.is_valid():                             # validate the form data
            username = signup_form.cleaned_data['username']
            name     = signup_form.cleaned_data['name']
            email    = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            new_user = UserModel(name=name, email=email, password=make_password(password), username=username)
            new_user.save()                                    # save data to db
            template_name = 'success.html'                     # rendering to success.html after post req
    return render(request,template_name, {'signup_form': signup_form})


def login_view(request):
    if request.method == 'GET':                                #display login form
        login_form = LoginForm()
        template_name = 'login.html'

    elif request.method == 'POST':                             # process the form data
        login_form = LoginForm(request.POST)
        if login_form.is_valid():                              # validation sucessful
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']     # read data from db
            user = UserModel.objects.filter(username=username).filter().first()
            if user:
                if check_password(password,user.password):     # compare the password
                    #login sucessful
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token',value=token.session_token)
                    return response
                else:
                    #login failed
                    template_name='login_fail.html'
            else:
                #user does not exist in db
                template_name = 'login_fail.html'
        else:
            # validation failed
            template_name='login_fail.html'
    return render(request,template_name,{'login_form':login_form})