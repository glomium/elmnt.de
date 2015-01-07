#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Technology


class TechnologyList(ListView):
    allow_empty = True

    def get_queryset(self):
        return Technology.active.all()


class TechnologyDetail(DetailView):

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.request, 'toolbar'):
            self.request.toolbar.set_object(self.object)
        return super(TechnologyDetail, self).get(*args, **kwargs)

    def get_queryset(self):
        return Technology.active.all()
