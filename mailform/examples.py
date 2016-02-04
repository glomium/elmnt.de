#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError

try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Layout, Div, HTML
    from crispy_forms.bootstrap import FormActions, StrictButton
    CRISPY = True
except ImportError:
    CRISPY = False


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_('Your name'),
        required=True,
        max_length=100,
    )
    email = forms.EmailField(
        label=_("Your email"),
        required=True,
    )
    subject = forms.CharField(
        label=_('Subject'),
        required=True,
        max_length=100,
    )
    message = forms.CharField(
        label=_('Message'),
        required=True,
        widget=forms.Textarea,
    )

    def __init__(self,*args,**kwargs):
        kwargs.update({'prefix': 'cnt'})
        super(ContactForm,self).__init__(*args,**kwargs)
        if CRISPY:
            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                'name',
                'email',
                'subject',
                'message',
                FormActions(
                      StrictButton(_('Reset'), type="reset", css_class="btn-default"),
                      StrictButton(_('Submit'), type="submit", css_class="btn-primary"),
                ),
            )

    def get_render_template(self):
        if CRISPY:
            return "mailform/crispy_form.html" 
        else:
            return "mailform/form_as_p.html" 

    def get_body_template(self):
        return "mailform/contact_body.txt" 

    def get_topic_template(self):
        return "mailform/contact_topic.txt" 
