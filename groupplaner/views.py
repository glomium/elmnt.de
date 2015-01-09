#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.timezone import now

from .models import Event, Participent
from .forms import ParticipentAnonymous
from .forms import ParticipentUser

class EventList(ListView):
    def get_queryset(self):
        return Event.objects.filter(end__gte=now())
    allow_empty = True

class EventDetail(SingleObjectTemplateResponseMixin, FormMixin, SingleObjectMixin, ProcessFormView):
    model = Event
    success_url = reverse_lazy('groupplaner-list')
  
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EventDetail, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EventDetail, self).post(request, *args, **kwargs)
  
    def get_form(self, form_class):
        if self.request.user.is_authenticated():
            try:
                data = self.object.participent_set.get(user=self.request.user)
                return ParticipentUser(instance=data,**self.get_form_kwargs())
            except Participent.DoesNotExist:
                return ParticipentUser(**self.get_form_kwargs())
        else:
            return ParticipentAnonymous(**self.get_form_kwargs())
    
    def form_valid(self,form):
        if self.request.user.is_authenticated():
            data = form.save(commit=False)
            data.user = self.request.user
            data.event = self.object
            data.save()
        else:
            data = form.save(commit=False)     
            try:
                pk = self.object.participent_set.get(name=form.cleaned_data['name'],user_id=None).pk
            except Participent.DoesNotExist:
                pk = None
            data.pk = pk
            data.event = self.object
            data.save()
        return super(EventDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        self.request._language_changer = lambda l: reverse('groupplaner-list')
        context = {'object': self.object}
        context.update(kwargs)
        return super(EventDetail, self).get_context_data(**context)
