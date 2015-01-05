#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import sitemaps

from .models import Technology

class TechnologySitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Technology.active.all()

    def lastmod(self, item):
        return item.changed

    def location(self, item):
        return item.get_absolute_url()
