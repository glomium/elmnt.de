#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Layout, Div, HTML
    from crispy_forms.bootstrap import FormActions, StrictButton
    from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
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
        label=_('Your message'),
        required=True,
        widget=forms.Textarea,
    )

    @property
    def helper(self):
        if not CRISPY:
            return None
        helper = FormHelper(self)
        helper.form_method = 'POST'
        helper.label_class = 'col-md-4 col-lg-3'
        helper.field_class = 'col-md-8 col-lg-9 m-b-1'

        helper.add_layout(Layout(
            Field('name', placeholder=_("Your name")),
            Field('email', placeholder=_("Your email")),
            Field('subject', placeholder=_("Subject")),
            Field('message', placeholder=_("Your message")),
            FormActions(
                  StrictButton(_('Reset'), type="reset", css_class="btn-default"),
                  StrictButton(_('Submit'), type="submit", css_class="btn-primary"),
                  css_class="text-right"
            ),
        ))
        return helper

    def get_render_template(self):
        if CRISPY:
            return "mailform/crispy_form.html" 
        else:
            return "mailform/form_as_p.html" 

    def get_body_template(self):
        return "mailform/contact_body.txt" 

    def get_topic_template(self):
        return "mailform/contact_topic.txt" 
