from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',

  url(r'^$',
    views.index,
    name='diet_index'),

  url(r'^graph/(?P<tag>.*)\.png$',
    views.graph,
    name='diet_graph'),

  url(r'^profile/$',
    views.profile,
    name='diet_profile'),

  url(r'^overview/$',
    views.overview,
    name='diet_overview'),

  url(r'^download$',
    views.download,
    name='diet_download'),

  url(r'^statistic/$',
    views.statistic,
    name='diet_statistic'),

  url(r'^statistic/(?P<year>\d{4})/(?P<month>\d{2})/$',
    views.statistic_month,
    name='diet_statistic_month'),

)

