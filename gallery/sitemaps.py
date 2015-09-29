#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import sitemaps

from .models import Photo


class GallerySitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "never"
    i18n = getattr(settings, 'USE_I18N', False)

    def items(self):
        return Photo.objects.all()

    def lastmod(self, item):
        return item.date

    def location(self, item):
        return item.get_absolute_url()
