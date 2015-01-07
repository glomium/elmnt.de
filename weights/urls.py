from django.conf.urls import url, patterns

from .views import IndexView
from .views import json

urlpatterns = patterns('',

  url(r'^$',
    IndexView.as_view(),
    name='weights-index'),

# url(r'^profile/$',
#   views.profile,
#   name='weights-profile'),

# url(r'^overview/$',
#   views.overview,
#   name='weights-overview'),

# url(r'^download$',
#   views.download,
#   name='weights-download'),

  url(r'^api/$',
    json,
    name='weights-api'),

  url(r'^api/(?P<year>\d{4})/$',
    json,
    name='weights-api'),

  url(r'^api/(?P<year>\d{4})/(?P<month>\d{2})/$',
    json,
    name='weights-api'),

)
