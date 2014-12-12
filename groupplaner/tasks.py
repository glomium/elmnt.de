#!/usr/bin/python
# ex:set fileencoding=utf-8:

from celery.schedules import crontab
from celery.task import periodic_task

from django.utils.timezone import now, make_aware, get_current_timezone

from datetime import datetime, timedelta

from .models import Event
from .models import WeeklyEvent

@periodic_task(run_every=crontab(hour='0',minute='0'))
def update():
    # date-range
    time = now()
    timerange = 14
    limit = time+timedelta(timerange)
    
    # read all weekly events and get days
    weekly = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[]} # weekdays
    for e in WeeklyEvent.objects.all():
        weekly[e.day].append( e )

    # read all events (connected to weekly)
    events = {}
    for e in Event.objects.filter(weekly__isnull=False,start__gt=time,end__lt=limit):
        key = str(e.start.date())
        try:
            events[key].append( e.weekly_id )
        except KeyError:
            events[key] = [e.weekly_id]

    # iterate over all days in range and compare both lists, and add event
    for i in range(timerange):
        d = (time+timedelta(i)).date()
        key = str(d)
        day = str(d.weekday())

        if key not in events:
            events[key] = []
           
        for w in weekly[day]:
            if not w.id in events[key]:
                E = Event()
                E.weekly      = w
                E.title       = w.title
                E.location    = w.location
                E.description = w.description
                E.start = datetime( d.year, d.month, d.day, w.start.hour, w.start.minute )
                E.end   = datetime( d.year, d.month, d.day, w.end.hour,   w.end.minute   )
                E.save()
