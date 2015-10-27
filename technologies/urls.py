#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf.urls import url, patterns

from .views import TechnologyList


urlpatterns = patterns('',
    url(r'^$', TechnologyList.as_view(), name='technologies-list'),
)
