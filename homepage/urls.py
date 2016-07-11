# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.contrib.sitemaps.views import index as sitemaps_index
from django.contrib.sitemaps.views import sitemap as sitemaps_sitemap
from django.views.static import serve

from importlib import import_module
from collections import OrderedDict


admin.autodiscover()


if getattr(settings, 'CMSTEMPLATE_I18N_URL', False) or len(getattr(settings, 'LANGUAGES', [])) > 1:
    from django.conf.urls.i18n import i18n_patterns
else:
    def i18n_patterns(*args):
        return args


SITEMAPS = {}
for key, modulepath in OrderedDict(sorted(getattr(settings, 'CMSTEMPLATE_SITEMAPS', {}).items())).items():
    module_path, class_name = modulepath.rsplit('.', 1)
    module = import_module(module_path)
    SITEMAPS[key] = getattr(module, class_name)


urlpatterns = [
    url(r'^sitemap\.xml$', sitemaps_index, {'sitemaps': SITEMAPS}),
    url(r'^sitemap-(?P<section>\w+)\.xml$', sitemaps_sitemap, {'sitemaps': SITEMAPS}),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ] + urlpatterns
