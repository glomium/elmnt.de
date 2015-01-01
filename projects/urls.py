#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf.urls import url, patterns

from .views import ProjectDetail
from .views import ProjectList


urlpatterns = patterns('',
    url(r'^$', ProjectList.as_view(), name='projects-list'),
    url(r'^(?P<slug>[\w_-]+)/$', ProjectDetail.as_view(), name='projects-detail'),
)
