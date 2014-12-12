#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import sitemaps
from django.utils.timezone import now
from django.utils.translation import activate

from .models import Event

class EventSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Event.objects.filter(end__gte=now())

    def lastmod(self, item):
        return item.changed

    def location(self, item):
        activate('de')  # TODO: this is stupid ...
        return item.get_absolute_url()
