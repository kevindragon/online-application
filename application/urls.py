from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'application.views.home', name='home'),
    # url(r'^application/', include('application.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'app.views.home'),
    url(r'^protocol/(?P<type_id>\d)', 'app.views.protocol'), 
    url(r'^job', 'app.views.jobs'),
    url(r'^apply/(?P<job_id>\d+)?', 'app.views.applyjob'), 
    url(r'^edit', 'app.views.edit'), 
    url(r'^update/', 'app.views.update'),
    url(r'^myinfo', 'app.views.myinfo'), 
    url(r'^progress', 'app.views.progress'), 
    url(r'^print/(?P<ptype>.*)', 'app.views.printinfo'), 
    url(r'^login/$', 'app.views.login'), 
    url(r'^logout/$', 'app.views.logout'), 
    url(r'^findpwd/$', 'app.views.findpwd'), 
    url(r'^changepwd/$', 'app.views.changepwd'),
    url(r'^uploadimage/$', 'app.views.uploadimage'), 
    
    url(r'^management/$', 'app.views.m_admin'), 
    url(r'^management/login/$', 'app.views.m_login'), 
    url(r'^management/logout/$', 'app.views.m_logout'),
    url(r'^management/people/del/$', 'app.views.m_people_del'), 
    url(r'^management/passwd/$', 'app.views.m_change_passwd'), 
    url(r'^management/job/$', 'app.views.m_job'), 
    url(r'^management/job/add/$', 'app.views.m_job_add'), 
    url(r'^management/job/(?P<job_id>\d+)/del/', 'app.views.m_job_del'), 
    url(r'^management/job/(?P<job_id>\d+)/edit/', 'app.views.m_job_edit'), 
    url(r'^management/audit/$', 'app.views.m_audit'), 
    url(r'^management/audit/(?P<people_id>\d+)/', 'app.views.m_audit'), 
    url(r'^management/people/(?P<people_id>\d+)', 'app.views.m_people'), 
    url(r'^management/plist/(?P<status>[^/]+)/(?P<page>\d+)/$', 'app.views.m_people_list'),
    url(r'^management/plist/(?P<status>.*)/$', 'app.views.m_people_list'),
    url(r'^management/stat/$', 'app.views.m_stat'), 
    url(r'^management/export/$', 'app.views.m_export'),
    url(r'^management/export/(?P<etype>.*)/', 'app.views.m_export'), 
    
    url(r'^admin/', include(admin.site.urls)), 
) + staticfiles_urlpatterns()
