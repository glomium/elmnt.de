#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib import admin
from models import WeeklyEvent, Event, Participent

admin.site.register(Event)
admin.site.register(WeeklyEvent)
admin.site.register(Participent)
