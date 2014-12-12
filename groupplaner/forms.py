#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django import forms
#from django.utils.translation import ugettext_lazy as _

#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Reset, Div

from .models import Participent

class ParticipentUser(forms.ModelForm):
  class Meta:
    model = Participent
    fields = (
                'status',
                'comment',
              )

class ParticipentAnonymous(forms.ModelForm):
  class Meta:
    model = Participent
    fields = (
                'name',
                'status',
                'comment',
              )
