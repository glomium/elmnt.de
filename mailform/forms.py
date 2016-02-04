#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from cms.models import Page
from django.forms.widgets import Media

from .models import Mailform

class MailformForm(ModelForm):
    try:
        from djangocms_link.fields import PageSearchField
        success_page = PageSearchField(queryset=Page.objects.drafts(), label=_("Success page"), required=False)
    except ImportError:
        from cms.forms.fields import PageSelectFormField
        success_page = PageSelectFormField(queryset=Page.objects.drafts(), label=_("Success page"), required=False)

    def for_site(self, site):
        # override the page_link fields queryset to containt just pages for
        # current site
        self.fields['success_page'].queryset = Page.objects.drafts().on_site(site)

    class Meta:
        model = Mailform
        include = ('site_email', 'formular' )
