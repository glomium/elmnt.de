#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf.urls import url, patterns

from .views import TechnologyDetail
from .views import TechnologyList


urlpatterns = patterns('',
    url(r'^$', TechnologyList.as_view(), name='technologies-list'),
    url(r'^(?P<slug>[\w_-]+)/$', TechnologyDetail.as_view(), name='technologies-detail'),
)
