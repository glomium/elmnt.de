from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView


from cms.sitemaps import CMSSitemap
from gallery.sitemaps import GallerySitemap
# from groupplaner.sitemaps import EventSitemap
from projects.sitemaps import ProjectSitemap

from django.contrib import admin
admin.autodiscover()

# from djangoerp import sites as djangoerp
# djangoerp.autodiscover()

SITEMAPS = {
    'cmspages': CMSSitemap,
    'gallery': GallerySitemap,
    # 'groupplaner': EventSitemap,
}

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
