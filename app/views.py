# -*- coding: utf-8 -*-

import hashlib
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
#from django.http import HttpResponse
from app.models import People, Job
from app.forms import PeopleForm, LoginForm

def home(request):
    peoples = People.objects.all()
    return render_to_response("home.html", locals())

def jobs(request):
    jobs = Job.objects.all()
    return render_to_response("jobs.html", locals())

def applyjob(request, job_id):
    locals().update(csrf(request))
    if request.method == 'POST':
        peopleForm = PeopleForm(request.POST)
        if peopleForm.is_valid():
            print "People Form is valided"
            data = peopleForm.cleaned_data
            data['query_password'] = hashlib.md5(data['query_password']).hexdigest()
            del data['query_password2']
            People(**data).save()
        else:
            print "People Form is invalided"
            return render_to_response("apply.html", locals())
    else:
        peopleForm = PeopleForm(initial={'job_id': job_id})
    return render_to_response("apply.html", locals())

def myinfo(request):
    if request.session.has_key('profile'):
        locals().update(csrf(request))
        people = request.session['profile']
        return render_to_response("myinfo.html", locals())
    else:
        return redirect('/login')

def login(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            id_number = loginForm.cleaned_data['id_number']
            password = loginForm.cleaned_data['password']
            people = People.objects.filter(id_number=id_number, 
                                           query_password=password)
            print 'people', people
            if people:
                request.session['profile'] = people[0]
                return redirect('/')
        else:
            print "invalid"
    else:
        loginForm = LoginForm()
    return render_to_response('login.html', locals())

def logout(request):
    del request.session['profile']
    return redirect('/')
