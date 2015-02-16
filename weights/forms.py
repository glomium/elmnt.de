#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Fieldset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Reset
from crispy_forms.layout import Submit

from .models import Data
from .models import Profile


class ProfileChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-editprofile'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(_('Settings'),
                'height',
                'dheight',
            ),
            ButtonHolder(
                Reset('reset', _('Reset')),
                Submit('submit', _('Save'), css_class="btn-primary"),
            )
        )
        super(ProfileChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = (
            'height',
            'dheight',
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
