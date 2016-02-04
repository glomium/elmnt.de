#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseRedirect

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Mailform
from .forms import MailformForm

class MailformPlugin(CMSPluginBase):
    model = Mailform
    form = MailformForm
    name = _("Mailformular")
    render_template = "mailform/form_as_p.html"
    body_template = "mailform/body.txt"
    topic_template = "mailform/topic.txt"
    cache = False
    # parent_classes = ['ColumnPlugin', 'MediaObjectPlugin']

    def render(self, context, instance, placeholder):
        request = context['request']
        component = instance.formular.split('.')

        try:
            mod = __import__('.'.join(component[:-1]), fromlist=[component[-1],])
        except ImportError:
            context.update({
                'error': _('Could not import the form'),
                'form': instance.formular,
            })
            return context

        formular = getattr(mod, component[-1])
        form = formular( request.POST or None )

        # overwrite default templates
        if hasattr(form, 'get_render_template'):
            tpl = form.get_render_template()
        else:
            tpl = None
        if isinstance(tpl, str) and tpl:
            self.render_template = tpl

        if hasattr(form, 'get_email_template'):
            tpl = form.get_email_template()
        else:
            tpl = None
        if isinstance(tpl, str) and tpl:
            self.body_template = tpl

        if hasattr(form, 'get_topic_template'):
            tpl = form.get_topic_template()
        else:
            tpl = None
        if isinstance(tpl, str) and tpl:
            self.topic_template = tpl

        if request.method == "POST" and form.is_valid():
            self.send(form, instance.site_email, attachments=request.FILES)
            context.update({
                'contact': instance,
                'success': True,
                'form': formular(None),
            })
            return context

        else:
            context.update({
                'contact': instance,
                'form': form,
            })
        return context

    def send(self, form, site_email, attachments=None):
        subject = render_to_string(self.topic_template, {'data': form.cleaned_data}).strip().splitlines()[0]
        body = render_to_string(self.body_template, {'data': form.cleaned_data, 'fields': form.fields})
        # TODO add template tag to get the select value of a choices field

        if 'email' in form.cleaned_data and form.cleaned_data['email']:
            email = form.cleaned_data['email']
        else:
            email = site_email
        
        if not subject:
            subject = 'Kein Betreff'

        email_message = EmailMessage(subject.encode("UTF8"), body.encode("UTF8"), email, [site_email], headers = {'Reply-To':email})

        if attachments:
            for var_name, data in attachments.iteritems():
                email_message.attach(data.name, data.read(), data.content_type)
        email_message.send(fail_silently=False)

plugin_pool.register_plugin(MailformPlugin)
