#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, Page

FORM_CHOICES = getattr(settings, 'CMSPLUGIN_MAILFORM_CHOICES', [
  ('cmsplugin_mailform.examples.ContactForm', 'Kontakt-Formular'),
])

@python_2_unicode_compatible
class Mailform(CMSPlugin):
    site_email = models.EmailField(
        _('Email recipient'),
    )
    formular = models.CharField(
        _('Formular'),
        default=FORM_CHOICES[0][0],
        choices=FORM_CHOICES,
        max_length=200,
    )
    success_page = models.ForeignKey(
        Page,
        verbose_name=_('Success page'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.formular
