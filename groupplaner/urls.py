#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf.urls import url, patterns

from .views import EventDetail
from .views import EventList

urlpatterns = patterns('',
  url(r'^$',EventList.as_view(),name='groupplaner-list'),
  url(r'^(?P<pk>[\d]+)/$',EventDetail.as_view(),name='groupplaner-detail'),
)
