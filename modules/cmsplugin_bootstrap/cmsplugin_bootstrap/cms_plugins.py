#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Row
from .models import Column
from .models import Well


class RowPlugin(CMSPluginBase):
    model = Row
    name = _("Row")
    render_template = "cmsplugin_bootstrap/row.html"
    require_parent = False
    allow_children = True
    child_classes = ['ColumnPlugin']

    if "cmsplugin_filer_image" in settings.INSTALLED_APPS:
        child_classes.append("FilerImagePlugin")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
plugin_pool.register_plugin(RowPlugin)


class ColumnPlugin(CMSPluginBase):
    model = Column
    name = _("Column")
    render_template = "cmsplugin_bootstrap/column.html"
    parent_classes = ['RowPlugin']
    allow_children = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['css'] = instance.get_css()
        return context
plugin_pool.register_plugin(ColumnPlugin)


class WellPlugin(CMSPluginBase):
    model = Well
    name = _("Well")
    render_template = "cmsplugin_bootstrap/well.html"
    allow_children = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['css'] = instance.get_css()
        return context
plugin_pool.register_plugin(WellPlugin)
