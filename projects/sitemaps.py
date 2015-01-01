#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import sitemaps

from .models import Project

class ProjectSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Project.active.all()

    def lastmod(self, item):
        return item.changed

    def location(self, item):
        return item.get_absolute_url()
