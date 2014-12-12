#!/usr/bin/python
# ex:set fileencoding=utf-8:
# ex:set textwidth=10000:

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Reset

from models import UserProfile, Data

class EditProfile(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'id-editprofile'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Fieldset(_('Settings'),
        'birth',
        'gender',
        'height',
        'dheight',
        'bmitarget',
      ),
      ButtonHolder(
        Reset('reset', _('Reset')),
        Submit('submit', _('Save'), css_class="btn-primary"),
      )
    )
    super(EditProfile, self).__init__(*args, **kwargs)

  class Meta:
    model = UserProfile
    fields = (
      'birth',
      'gender',
      'height',
      'dheight',
      'bmitarget',
    )


class DataForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'id-dataform'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Fieldset(_('Weight'),
        'weight',
      ),
      ButtonHolder(
        Reset('reset', _('Reset')),
        Submit('submit', _('Save'), css_class="btn-primary"),
      )
    )
    super(DataForm, self).__init__(*args, **kwargs)

  class Meta:
    model = Data
    fields = (
      'weight',
    )

