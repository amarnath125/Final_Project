# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from demoapp.forms import SignUpForm,LoginForm,PostForm
from django.contrib.auth.hashers import make_password,check_password   # make_password is used to encrypt the pswrd
from demoapp.models import UserModel,SessionToken,PostModel
from imgurpython import ImgurClient
from mydjangoproject.settings import BASE_DIR


# Create your views here.

def check_user(request):
    if request.COOKIES.get("session_token"):
        session = SessionToken.objects.filter(session_token = request.COOKIES.get('session_token')).first()
        if session:
            return session.user
        else:
            return None



def logout_view(request):
    user_id = check_user(request)
    delete_user = SessionToken.objects.filter(user = user_id)
    delete_user.delete()
    return redirect('/signup/')



def feed_view(request):
    user = check_user(request)
    if user == None:
        return redirect('/login/')
    elif request.method == 'GET':
        post_form=PostForm()
        return render(request,'feed.html',{'post_form':post_form})
    elif request.method == "POST":
        form =PostForm(request.POST,request.FILES)
        if form.is_valid():
            image   = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            post    = PostModel(user=user, image=image, caption=caption)
            post.save()                     #saving image, caption
            client  = ImgurClient('a6ef522b68f01a9','7d31b3b76ad618f8e97f8951ed87b25b5f87572b')
            path    = str(BASE_DIR) + '\\' + str(post.image)
            post.image_url = client.upload_from_path(path,anon=True)['link']
            post.save()                     #saving url
            #print post.image_url
            #print post.image
            return redirect('/feed/')



def login_view(request):
    if request.method == 'GET':                                #display login form
        login_form = LoginForm()
        template_name = 'login.html'

    elif request.method == 'POST':                             # process the form data
        login_form = LoginForm(request.POST)
        if login_form.is_valid():                              # validation sucessful
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']     # read data from db
            user = UserModel.objects.filter(username=username).first()
            if user:
                if check_password(password,user.password):     # compare the password
                    #login sucessful
                    token = SessionToken(user=user)
                    token.create_token()                        #calling to create_token()
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
        else:
            dict={"key":"Pleas fill the form"}
            return render(request,'signup.html',dict)


    return render(request,template_name, {'signup_form': signup_form})
