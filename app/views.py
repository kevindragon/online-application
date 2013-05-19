# -*- coding: utf-8 -*-

import hashlib, string, random, os, shutil, time
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from app.models import People, Job, PeopleExtra
from app.forms import PeopleForm, LoginForm, PeopleNoPasswordForm, FindpwdForm 
from app.forms import ChangepwdForm, AdminLoginForm, AdminChangePasswd, JobForm
from app.forms import AuditForm

def auth_check(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.session.has_key('profile'):
            return redirect('/login')
        request.session.set_expiry(3600)
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
            data['audit_step'] = 0
            data['query_password'] = hashlib.md5(data['query_password']).hexdigest()
            del data['query_password2']
            
            # 复制图片到相应目录
            avatar_path = "/".join(('static/upload/', peopleForm.cleaned_data["id_number"]))
            if not os.path.exists(avatar_path):
                os.mkdir(avatar_path)
            src_file = peopleForm.cleaned_data["avatar"][1:]
            dst_file = "/".join((avatar_path, os.path.basename(peopleForm.cleaned_data["avatar"])))
            if src_file!=dst_file:
                try:
                    shutil.move(src_file, dst_file)
                    peopleForm.cleaned_data["avatar"] = '/%s' % (dst_file, )
                except Exception:
                    pass
            
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
        return redirect('/myinfo/')
    locals().update(csrf(request))

@auth_check
def update(request):
    locals().update(csrf(request), operate='edit')
    if request.method == 'POST':
        peopleForm = PeopleNoPasswordForm(request.POST)
        if (request.POST.get('id_number') == request.session['profile'].id_number and 
            peopleForm.is_valid()):
            data = peopleForm.cleaned_data
            data['audit_step'] = 0
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
    people = People.objects.get(pk=request.session['profile'].id)
    if ptype == 'audit':
        return render_to_response("audit_table.html", locals())
    else:
        return render_to_response("ticket_table.html", locals())

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
                request.session.set_expiry(3600)
                return redirect('/')
    else:
        loginForm = LoginForm()
    return render_to_response('login.html', locals())

def logout(request):
    if request.session.has_key('profile'):
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
                subject = (u'找回%s在内蒙古工业大学申请的 %s(%s) 的查询密码' % 
                           (people[0].name, people[0].job.major, people[0].job.job_type))
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
                form.errors['__all__'] = form.error_class([u'未能匹配身份证号与电子邮箱'])
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

def protocol(request, type_id):
    return render_to_response("protocol.html", locals())

def uploadimage(request):
    filename = request.FILES['avatar'].name
    filedata = request.FILES['avatar']
    prefix, suffix = os.path.splitext(filename)
    if filedata.file:
        filename = (
            "static/upload/tmp/%s%s" % 
            (hashlib.md5(str(time.time())).hexdigest(),
             "%s%s" % (hashlib.md5(str(time.time())).hexdigest(), suffix)))
        open(filename, "wb").write(filedata.read())
    for root, dirs, files in os.walk("static/upload/tmp/"):
        for filespath in files:
            tmpfilename = "%s/%s" % (root, filespath)
            if time.time() - os.stat(tmpfilename).st_mtime > 86400:
                os.unlink(tmpfilename)
    return HttpResponse("/%s" % filename)

# ---------- admin views ----------

def m_auth_check(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return redirect('/management/login/')
        return func(*args, **kwargs)
    return wrapper

@m_auth_check
def elementary(request):
    locals().update(csrf(request))
    peoples = People.objects.filter(audit_step__lt=1)
    if request.session.has_key('message'):
        message = request.session['message']
        del request.session['message']
    return render_to_response("m_elementary.html", locals())

@m_auth_check
def m_people_del(request):
    if request.method == 'POST' and request.POST.get('operate') == 'del':
        people_ids = request.POST.getlist('people_id')
        peoples = People.objects.filter(pk__in=people_ids)
        peoples.delete()
        request.session['message'] = u'删除成功'
        return redirect('/management/elementary/')

@m_auth_check
def m_audit(request, people_id=0):
    locals().update(csrf(request))
    if request.method == 'POST':
        people = People.objects.get(pk=request.POST.get('people'))
        form = AuditForm(people, request.POST)
        if form.is_valid():
            form.save()
            people.audit_step = form.cleaned_data['audit_step']
            people.save()
            request.session['message'] = u'%s的审核状态保存成功' % (people.name, )
            return redirect('/management/elementary/')
    else:
        people = People.objects.get(pk=people_id)
        job = Job.objects.get(pk=people.job.id)
        failed_audit = ('7', '8')
        if people.audit_step >= 0:
            audit_step = (people.audit_step, 7, 8)
            people_extra = PeopleExtra.objects.filter(people=people, audit_step__in=audit_step)
        form = AuditForm(people, initial={'people': people})
    return render_to_response("m_audit.html", locals())

@m_auth_check
def m_admin(request):
    return render_to_response("m_admin.html", locals())

@m_auth_check
def m_job(request):
    '''岗位列表'''
    locals().update(csrf(request))
    jobs = Job.objects.all()
    if request.session.has_key('message'):
        message = request.session['message']
        del request.session['message']
    return render_to_response("m_job_list.html", locals())

@m_auth_check
def m_job_add(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            if request.POST.get('edit') == '1':
                job = Job.objects.get(pk=int(request.POST.get('job_id')))
                for k, v in form.cleaned_data.items():
                    setattr(job, k, v)
                job.save()
                request.session['message'] = u'岗位信息修改成功'
            else:
                form.save()
                request.session['message'] = u'岗位信息添加成功'
            return redirect("/management/job/")
    else:
        form = JobForm()
    return render_to_response("m_job_add.html", locals())

@m_auth_check
def m_job_del(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.delete()
    request.session['message'] = u'%s - %s删除成功' % (job.major, job.job_type)
    return redirect("/management/job/")

@m_auth_check
def m_job_edit(request, job_id):
    locals().update(csrf(request))
    job = Job.objects.get(pk=job_id)
    form = JobForm(instance=job)
    edit = True
    return render_to_response("m_job_add.html", locals())

def m_change_passwd(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        form = AdminChangePasswd(request.POST)
        if form.is_valid() and request.user.check_password(request.POST.get('old_passwd')):
            request.user.set_password(request.POST.get('new_passwd'))
            request.user.save()
            message = u'密码修改成功'
            return render_to_response("m_msg.html", locals())
    else:
        form = AdminChangePasswd()
    return render_to_response("m_passwd.html", locals())

def m_login(request):
    locals().update(csrf(request))
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), 
                                password=request.POST.get('password'))
            if user and user.is_active:
                auth.login(request, user)
                return redirect("/management/")
    else:
        form = AdminLoginForm()
    return render_to_response("m_login.html", locals())

def m_logout(request):
    auth.logout(request)
    return redirect("/management/login/")



