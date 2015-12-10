#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Section


class SectionPlugin(CMSPluginBase):
    model = Section
    module = _("Bootstrap4")
    name = _("Section")
    render_template = "bootstrap4/section.html"
    allow_children = True
#   require_parent = True

    def render(self, context, instance, placeholder):
        context['css'] = instance.get_css()
        context['instance'] = instance
        return context
plugin_pool.register_plugin(SectionPlugin)

#rom .models import Row
#rom .models import Column
#rom .models import Well


#lass RowPlugin(CMSPluginBase):
#   model = Row
#   name = _("Row")
#   render_template = "bootstrap4/row.html"
#   require_parent = False
#   allow_children = True
#   child_classes = ['ColumnPlugin']

#   if "cmsplugin_filer_image" in settings.INSTALLED_APPS:
#       child_classes.append("FilerImagePlugin")

#   def render(self, context, instance, placeholder):
#       context['instance'] = instance
#       return context
#lugin_pool.register_plugin(RowPlugin)


#lass ColumnPlugin(CMSPluginBase):
#   model = Column
#   name = _("Column")
#   render_template = "bootstrap4/column.html"
#   parent_classes = ['RowPlugin']
#   allow_children = True

#   def render(self, context, instance, placeholder):
#       context['instance'] = instance
#       context['css'] = instance.get_css()
#       return context
#lugin_pool.register_plugin(ColumnPlugin)


#lass WellPlugin(CMSPluginBase):
#   model = Well
#   name = _("Well")
#   render_template = "cmsplugin_bootstrap/well.html"
#   allow_children = True

#   def render(self, context, instance, placeholder):
#       context['instance'] = instance
#       context['css'] = instance.get_css()
#       return context
#lugin_pool.register_plugin(WellPlugin)
