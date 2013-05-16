from django.contrib import admin
from app.models import Job, People, PeopleExtra

admin.site.register(Job)
admin.site.register(People)
admin.site.register(PeopleExtra)