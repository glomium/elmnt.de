from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',

  url(r'^$',
    views.index,
    name='weights-index'),

  url(r'^graph/(?P<tag>.*)\.png$',
    views.graph,
    name='weights-graph'),

  url(r'^profile/$',
    views.profile,
    name='weights-profile'),

  url(r'^overview/$',
    views.overview,
    name='weights-overview'),

  url(r'^download$',
    views.download,
    name='weights-download'),

  url(r'^statistic/$',
    views.statistic,
    name='weights-statistic'),

  url(r'^statistic/(?P<year>\d{4})/(?P<month>\d{2})/$',
    views.statistic_month,
    name='weights-statistic-month'),

)
