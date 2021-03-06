#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf.urls import url

from .views import PhotoListView
from .views import PhotoDetailView

urlpatterns = [
    url(
        r'^$',
        PhotoListView.as_view(),
        name='gallery-index',
    ),
    url(
        r'^picture/(?P<slug>[-\w]+)/$',
        PhotoDetailView.as_view(),
        name='gallery-picture',
    ),
]
