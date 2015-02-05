#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

import csv

from .models import Profile
from .models import Data


class IndexView(TemplateView):
    template_name = "weights/index.html"


@login_required
@never_cache
def json(request, year=None, month=None):
    profile = get_object_or_404(Profile, user=request.user)

    objs = profile.data.all()

    response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename=data.csv'

    writer = csv.writer(response)
    writer.writerow([
        'date',
        'weight',
        'cweight_h',
        'cweight_l',
        'mid',
    ])

    for obj in objs:
        writer.writerow([
#           obj.date.isoformat(),
            obj.date.strftime('%Y-%m-%d %H:%M:%S'),
            '%5.2f' % float(obj.weight),
            '%5.2f' % (obj.calc_vweight + obj.calc_dweight),
            '%5.2f' % (obj.calc_vweight - obj.calc_dweight),
            '%5.2f' % (0.5 * obj.max_weight + 0.5 * obj.min_weight),
    ])

    return response


"""
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.views.decorators.cache import cache_control

from datetime import datetime, timedelta

from models import UserProfile, Month, Data, Graph
from forms import EditProfile, DataForm
from context_processors import extra_content

from glomium.documents.views import sendfile

def get_extra_content(request, login=True, profile=True):
  c = {
  }
  return c

@login_required
def index(request):
  c = {}
  try:
    u = UserProfile.objects.get(user=request.user)
    return HttpResponseRedirect( reverse('diet_statistic') )
  except UserProfile.DoesNotExist:
    return render_to_response('diet/noprofile.html',c,context_instance=RequestContext(request))

@login_required
@cache_control(must_revalidate=True, private=True)
def graph(request,tag):
  graph = get_object_or_404(Graph, user_id=request.user.pk, pretag=tag)
  return sendfile(request,graph.image.url)

@login_required
def profile(request):
  ''' show and edit profile '''
  c = {}
  try:
    profile = UserProfile.objects.get(user=request.user)
  except UserProfile.DoesNotExist:
    profile = None

  form=EditProfile(request.POST or None, instance=profile)

  if form.is_valid():
    user = form.save(commit=False)
    user.user = request.user
    user.save()
    # TODO message profil saved 
    return HttpResponseRedirect( reverse('diet_statistic') )
  c['form'] = form
  return render_to_response('diet/profile.html',c,context_instance=RequestContext(request,{},[extra_content]))

@login_required
def overview(request):
  ''' overviews all data '''
  c = {
    'table': Month.objects.filter(user_id=request.user.pk),
  }
  return render_to_response('diet/overview.html',c,context_instance=RequestContext(request,{},[extra_content]))

@login_required
def statistic(request):
  ''' statistic oberviews (month-tables) '''
  profile = get_object_or_404(UserProfile,user=request.user)

  # get user Objects
  try:
    data = Data.objects.get(user=request.user, date=now())
  except Data.DoesNotExist:
    data = None

# if request.method == 'POST':
#   # load form
#   f = DietDataForm(request.POST, instance=u)

#   if f.is_valid():
#     dietuser = f.save(commit=False)
#     dietuser.user = request.user
#     dietuser.save()
#     c['formsave'] = "Daten erfolgreich gespeichert"
# else:
#   f = DietDataForm(instance=u)
# c['form'] = f

# try:
#   img = DietGraph.objects.get(user=request.user, pretag='stats')
# except:
#   img = DietGraph(user=request.user, pretag='stats')
# c['img'] = img

# try:
#   q = DietData.objects.filter(user=request.user).latest('date')
# except DietData.DoesNotExist:
#   q = u
#
# c['dietstats'] = q.get_stats(profile=profile)

  c = {
  }
 
  return render_to_response('diet/statistic.html',c,context_instance=RequestContext(request,{},[extra_content]))

@login_required
def statistic_month(request, year, month):
  ''' statistic oberviews (monthly details) '''
  c = get_extra_content(request)
  c['data'] = get_object_or_404(DietMonth, user=request.user, date__year=year, date__month=month)
  select = str(month)+'-'+str(year)
  try:
    img = DietGraph.objects.get(user=request.user, pretag=select)
  except:
    img = DietGraph(user=request.user, pretag=select)
  c['img'] = img
  return render_to_response('diet/statistic_month.html',c,context_instance=RequestContext(request))

"""
