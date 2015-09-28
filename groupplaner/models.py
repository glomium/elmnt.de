#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

WEEKDAY_CHOICES = (
    ('0', _('Monday')),
    ('1', _('Tuesday')),
    ('2', _('Wednesday')),
    ('3', _('Thursday')),
    ('4', _('Friday')),
    ('5', _('Saturday')),
    ('6', _('Sunday')),
)

STATUS_YES = 1
STATUS_MAYBE = 3
STATUS_NO = 5
STATUS_CHOICES = (
    (STATUS_YES,   _('yes')),
    (STATUS_MAYBE, _('maybe')),
    (STATUS_NO,    _('no')),
)

# ========================================================================

class WeeklyEvent(models.Model):
    day = models.CharField(
        _('day'),
        max_length=1,
        choices=WEEKDAY_CHOICES,
        blank=False,
    )
    title = models.CharField(
        _('title'),
        max_length=100,
        blank=False,
    )
    location = models.CharField(
        _('location'),
        max_length=100,
        blank=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    start = models.TimeField(
        _('start'),
        blank=False,
    )
    end = models.TimeField(
        _('end'),
        blank=False,
    )
    active = models.BooleanField(
        _('active'),
        default=True,
    )

    def __unicode__(self):
        return "%s: %s (%s)"%(self.day,self.title,self.location)

    class Meta:
        verbose_name_plural = _('Weekly events')
        verbose_name = _('Weekly event')
        ordering = ['active','day','start','end']

# ========================================================================

class Event(models.Model):
    weekly = models.ForeignKey(
        WeeklyEvent,
        null=True,
        blank=True,
        related_name="+",
    )
    title = models.CharField(
        _('title'),
        max_length=100,
        blank=False,
    )
    location = models.CharField(
        _('location'),
        max_length=100,
        blank=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    start = models.DateTimeField(
        _('start'), 
        blank=False,
    )
    end = models.DateTimeField(
        _('end'), 
        blank=False,
    )
    changed = models.DateTimeField(
        _('changed'),
        auto_now=True,
    )
    added = models.DateTimeField(
        _('added'),
        auto_now_add=True,
    )

    def __unicode__(self):
        return "%s: %s"%(self.start,self.title)

    def days(self):
        if self.start.date() == self.end.date():
            return False
        else:
            return True

    def check_participents(self):
        count = Participent.objects.filter(event=self.pk).count()
        if count > 0:
            return True
        else:
            return False

    def get_participents(self):
        return Participent.objects.filter(event=self.pk)

    class Meta:
        verbose_name_plural = _('Events')
        verbose_name = _('Event')
        ordering = ['start','end']

    @models.permalink
    def get_absolute_url(self):
        return ('groupplaner-detail', None, {
            'pk': self.pk
        })

# ========================================================================

class Participent(models.Model):
    event = models.ForeignKey(
        Event, 
    )
    user = models.ForeignKey(
        User, # TODO: add new User model
        null=True,
        blank=True,
        related_name="+",
    )
    name = models.CharField(
        _('name'),
        max_length=40,
        null=False,
        blank=False,
    )
    status = models.PositiveSmallIntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        blank=False,
        default=STATUS_YES,
    )
    comment = models.CharField(
        _('comment'),
        max_length=255,
        null=False,
        blank=True,
    )

    class Meta:
        verbose_name_plural = _('Participents')
        verbose_name = _('Participent')
        ordering = ['event','status']

    def __unicode__(self):
        return u"%s (%s)"%(self.get_status(color=False), self.get_status_display())

    def get_status(self,color=True):
        if self.user:
            name = '%s %s.'%(self.user.first_name, self.user.last_name[0:1]) # TODO: change user model
        else:
            name = '%s'%(self.name)

        if not color:
            return name

        status = 'black'
        if self.status == STATUS_YES:
            status = 'green'
        if self.status == STATUS_MAYBE:
            status = 'orange'
        if self.status == STATUS_NO:
            status = 'red'

        if self.user:
            return '<li><b style="color:%s;"><u>%s</u></b> %s</li>'%(status,name,self.comment) 
        else:
            return '<li><b style="color:%s;">%s</b> %s</li>'%(status,name,self.comment) 
