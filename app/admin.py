from django.contrib import admin
from app.models import Job, People, PeopleExtra, LockedStatus

admin.site.register(Job)
admin.site.register(People)
admin.site.register(PeopleExtra)
admin.site.register(LockedStatus)