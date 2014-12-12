#!/usr/bin/python
# ex:set fileencoding=utf-8:

from models import Month

def extra_content(request):
  context_extras = {
    'statistic': Month.objects.filter(user=request.user)[0:12],
  }
  return context_extras

