# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from importlib import import_module
admin.autodiscover()


if getattr(settings, 'CMSTEMPLATE_I18N_URL', False) or len(getattr(settings, 'LANGUAGES', [])) > 1:
    from django.conf.urls.i18n import i18n_patterns
else:
    i18n_patterns = patterns


SITEMAPS = {}
for key, modulepath in getattr(settings, 'CMSTEMPLATE_SITEMAPS', {}).items():
    module_path, class_name = modulepath.rsplit('.', 1)
    module = import_module(module_path)
    SITEMAPS[key] = getattr(module, class_name)


urlpatterns = patterns(
    'django.contrib.sitemaps.views',
    url(r'^sitemap\.xml$', 'index', {'sitemaps': SITEMAPS}),
    url(r'^sitemap-(?P<section>\w+)\.xml$', 'sitemap', {'sitemaps': SITEMAPS}),
)

urlpatterns += patterns(
    '',
    url(r'^en', RedirectView.as_view(url='/', permanent=True)),
)

urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
