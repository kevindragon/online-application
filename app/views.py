# -*- coding: utf-8 -*-

import hashlib, string, random
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from app.models import People, Job
from app.forms import PeopleForm, LoginForm, PeopleNoPasswordForm, FindpwdForm 
from app.forms import ChangepwdForm

def auth_check(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.session.has_key('profile'):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

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
            data = peopleForm.cleaned_data
            data['query_password'] = hashlib.md5(data['query_password']).hexdigest()
            del data['query_password2']
            People(**data).save()
            return render_to_response("msg.html", {'message': u'信息提交成功'})
    else:
        peopleForm = PeopleForm(initial={'job': job_id})
    return render_to_response("apply.html", locals())

@auth_check
def edit(request):
    profile = request.session['profile']
    if request.POST.get('id_number')==profile.id_number:
        peopleForm = PeopleNoPasswordForm(instance=profile)
        peopleForm.fields['id_number'].widget.attrs['readonly'] = True
        locals().update(csrf(request), operate='edit')
        return render_to_response("apply.html", locals())
    else:
        return redirect('/myinfo')
    locals().update(csrf(request))

@auth_check
def update(request):
    locals().update(csrf(request), operate='edit')
    if request.method == 'POST':
        peopleForm = PeopleNoPasswordForm(request.POST)
        if (request.POST.get('id_number') == request.session['profile'].id_number and 
            peopleForm.is_valid()):
            data = peopleForm.cleaned_data
            # 把不需要更新的字段去掉
            del data['id_number'], data['query_password']
            people = People.objects.get(pk=request.session['profile'].id)
            for k, v in data.items():
                setattr(people, k, v)
            people.save()
            # 更新session
            request.session['profile'] = people
            message = u'信息修改成功。<a href="/myinfo">查看</a>'
            return render_to_response("msg.html", locals())
        return render_to_response("apply.html", locals())
    else:
        return redirect('/')

@auth_check
def myinfo(request):
    locals().update(csrf(request))
    people = People.objects.get(pk=request.session['profile'].id)
    return render_to_response("myinfo.html", locals())

@auth_check
def progress(request):
    people = People.objects.get(pk=request.session['profile'].id)
    return render_to_response("progress.html", locals())

@auth_check
def printinfo(request, ptype):
    return render_to_response("audit_table.html", locals())

def login(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            people = People.objects.filter(
                id_number=loginForm.cleaned_data['id_number'], 
                query_password=hashlib.md5(loginForm.cleaned_data['password']).hexdigest()
            )
            if people:
                request.session['profile'] = people[0]
                return redirect('/')
    else:
        loginForm = LoginForm()
    return render_to_response('login.html', locals())

def logout(request):
    del request.session['profile']
    return redirect('/')

def findpwd(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        form = FindpwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            people = People.objects.filter(id_number=data['id_number'], email=data['email'])
            if people:
                pwd = ''.join(random.choice(string.letters + string.digits) for x in range(12))
                pwdhash = hashlib.md5(pwd).hexdigest()
                subject = u'找回%s在内蒙古工业大学申请的%s的查询密码' % (people[0].name, people[0].job.title)
                msg = ((u"亲爱的%s\n\n您的查询密码已经被系统重置，请使用下面的密码登录\n\n"
                        u"%s\n\nhttp://localhost:8000/login") % 
                       (people[0].name, pwd))
                is_sent = send_mail(subject, msg, settings.ADMIN_EMAIL, [people[0].email])
                if is_sent:
                    people[0].query_password = pwdhash
                    people[0].save()
                    message = u'您的密码已经发送到您的邮箱，请登录您的邮箱查看'
                else:
                    message = u'邮件发送失败，请联系内蒙古工业大学人事处00000-0000000'
                return render_to_response("msg.html", locals())
    else:
        form = FindpwdForm()
    return render_to_response("findpwd.html", locals())

@auth_check
def changepwd(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            old_query_password = hashlib.md5(form.cleaned_data['old_password']).hexdigest()
            people = People.objects.filter(pk=request.session['profile'].id, 
                                           query_password=old_query_password)
            if people:
                query_password = hashlib.md5(form.cleaned_data['new_password']).hexdigest()
                people[0].query_password = query_password
                people[0].save()
                message = u'密码修改成功'
                return render_to_response("msg.html", locals())
            else:
                form.errors['old_password'] = form.error_class([u'原始密码不匹配'])
    else:
        form = ChangepwdForm()
    return render_to_response("changepwd.html", locals()) 


