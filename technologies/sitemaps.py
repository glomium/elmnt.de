#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import sitemaps

from .models import Technology


class TechnologySitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    i18n = getattr(settings, 'USE_I18N', False)

    def items(self):
        return Technology.active.all()

    def lastmod(self, item):
        return item.modified

    def location(self, item):
        return item.get_absolute_url()
