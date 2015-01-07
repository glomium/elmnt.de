#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Project


class ProjectList(ListView):
    allow_empty = True

    def get_queryset(self):
        return Project.active.all()


class ProjectDetail(DetailView):

    def get_queryset(self):
        return Project.active.all()
