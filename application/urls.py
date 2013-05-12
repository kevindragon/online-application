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

    # Uncomment the next line to enable the admin:
    url(r'^$', 'app.views.home'),
    url(r'^job', 'app.views.jobs'),
    url(r'^apply/(?P<job_id>\d+)?', 'app.views.applyjob'), 
    url(r'^edit', 'app.views.edit'), 
    url(r'^update/', 'app.views.update'),
    url(r'^myinfo', 'app.views.myinfo'), 
    url(r'^progress', 'app.views.progress'), 
    url(r'^print/(?P<ptype>.*)', 'app.views.printinfo'), 
    url(r'^login', 'app.views.login'), 
    url(r'^logout', 'app.views.logout'), 
    url(r'^findpwd', 'app.views.findpwd'), 
    url(r'^changepwd', 'app.views.changepwd'), 
    url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()
