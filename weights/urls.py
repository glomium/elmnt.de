from django.conf.urls import url
from django.conf.urls import patterns

from .views import IndexView
from .views import DataCreateView
from .views import DataDeleteView
from .views import DataUpdateView
from .views import ProfileUpdateView
from .views import csv_view

urlpatterns = patterns('',
    url(
        r'^$',
        IndexView.as_view(),
        name='weights-index',
    ),
    url(
        r'^api/$',
        csv_view,
        name='weights-api',
    ),
    url(
        r'^api/(?P<year>\d{4})/$',
        csv_view,
        name='weights-api',
    ),
    url(
        r'^api/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        csv_view,
        name='weights-api',
    ),
    url(
        r'^create/$',
        DataCreateView.as_view(),
        name='weights-create',
    ),
    url(
        r'^delete/$',
        DataDeleteView.as_view(),
        name='weights-delete',
    ),
    url(
        r'^update/$',
        DataUpdateView.as_view(),
        name='weights-update',
    ),
    url(
        r'^profile/$',
        ProfileUpdateView.as_view(),
        name='weights-profile',
    ),
)
