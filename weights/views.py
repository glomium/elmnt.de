#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from datetime import timedelta

import csv

from .models import Profile
from .models import Data
from .forms import ProfileChangeForm
from .forms import DataForm


class AppMixin(object):

    def load_app(self):
        if hasattr(self, 'app_loaded'):
            return None
        if self.request.user.is_anonymous():
            self.profile = None
            self.latest_data = None
            self.navigation = None
        else:
            try:
                self.profile = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                self.profile = None

            try:
                self.latest_data = self.profile.data.order_by('-date').first()
                self.navigation = self.profile.data.datetimes('date', 'month', 'DESC')
            except AttributeError:
                self.latest_data = None
                self.navigation = None
        self.app_loaded = True

    def get_context_data(self, **kwargs):
        self.load_app()
        kwargs.update({
            'profile': self.profile,
            'navigation': self.navigation,
            'latest_data': self.latest_data,
        })

        return super(AppMixin, self).get_context_data(**kwargs)


class AppFormMixin(object):

    def dispatch(self, *args, **kwargs):
        self.load_app()
        if not self.profile:
            raise Http404
        return super(AppFormMixin, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('weights-index')


class IndexView(AppMixin, AppFormMixin, TemplateView):
    template_name = "weights/index.html"


class DataCreateView(AppMixin, AppFormMixin, CreateView):
    model = Data
    form_class = DataForm

    def form_valid(self, form):
        form.instance.user = self.profile
        form.instance.date = now()
        return super(DataCreateView, self).form_valid(form)


class DataDeleteView(AppMixin, AppFormMixin, DeleteView):
    model = Data

    def get_object(self):
        return self.latest_data


class DataUpdateView(AppMixin, AppFormMixin, UpdateView):
    model = Data
    form_class = DataForm

    def get_object(self):
        return self.latest_data

    def form_valid(self, form):
        form.instance.date = now()
        return super(DataUpdateView, self).form_valid(form)


class ProfileUpdateView(AppMixin, AppFormMixin, UpdateView):
    model = Profile
    form_class = ProfileChangeForm

    def get_object(self):
        return self.profile


@login_required
@never_cache
def csv_view(request, year=None, month=None):
    profile = get_object_or_404(Profile, user=request.user)

    if not year and not month:
        objs = profile.data.filter(date__gt=now()-timedelta(31))
    else:
        objs = profile.data.filter(date__year=year)
        if month:
            objs = objs.filter(date__month=month)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'

    writer = csv.writer(response)
    writer.writerow([
        'date',
        'weight',
        'cweight_h',
        'cweight',
        'cweight_l',
        'mid',
        'slope_h',
        'slope',
        'slope_l',
    ])

    for obj in objs:
        writer.writerow([
#           obj.date.isoformat(),
            obj.date.strftime('%Y-%m-%d %H:%M:%S'),
            '%6.3f' % float(obj.weight),
            '%6.3f' % (obj.calc_vweight + obj.calc_dweight),
            '%6.3f' % (obj.calc_vweight),
            '%6.3f' % (obj.calc_vweight - obj.calc_dweight),
            '%6.3f' % (0.5 * obj.max_weight + 0.5 * obj.min_weight),
            '%4.3f' % (obj.calc_vslope + obj.calc_dslope),
            '%4.3f' % (obj.calc_vslope),
            '%4.3f' % (obj.calc_vslope - obj.calc_dslope),
    ])

    return response
