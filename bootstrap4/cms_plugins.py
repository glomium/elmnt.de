#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Section
from .models import Row
from .models import Column
from .models import ColumnClearfix
from .models import MediaObject
from .models import Image
from .models import Embed


class SectionPlugin(CMSPluginBase):
    model = Section
    module = _("Bootstrap4")
    name = _("Section")
    render_template = "bootstrap4/section.html"
    child_classes = ['RowPlugin', 'EmbedPlugin', 'TextPlugin', 'ImagePlugin', 'MediaObjectPlugin']
    allow_children = True
    require_parent = False

    def render(self, context, instance, placeholder):
        context['css'] = instance.get_css()
        context['instance'] = instance
        return context
plugin_pool.register_plugin(SectionPlugin)


class RowPlugin(CMSPluginBase):
    model = Row
    module = _("Bootstrap4")
    name = _("Row")
    render_template = "bootstrap4/row.html"
    require_parent = True
    allow_children = True
    child_classes = ['ColumnPlugin', 'ColumnClearfixPlugin']

#   if "cmsplugin_filer_image" in settings.INSTALLED_APPS:
#       child_classes.append("FilerImagePlugin")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
plugin_pool.register_plugin(RowPlugin)


class ColumnPlugin(CMSPluginBase):
    model = Column
    module = _("Bootstrap4")
    name = _("Column")
    render_template = "bootstrap4/column.html"
    parent_classes = ['RowPlugin']
    allow_children = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['css'] = instance.get_css()
        return context
plugin_pool.register_plugin(ColumnPlugin)


class ColumnClearfixPlugin(CMSPluginBase):
    model = ColumnClearfix
    module = _("Bootstrap4")
    name = _("Column Clearfix")
    render_template = "bootstrap4/columnclearfix.html"
    parent_classes = ['RowPlugin']
    allow_children = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
plugin_pool.register_plugin(ColumnClearfixPlugin)


class MediaObjectPlugin(CMSPluginBase):
    model = MediaObject
    module = _("Bootstrap4")
    name = _("MediaObject")
    render_template = "bootstrap4/mediaobject.html"
    parent_classes = ['ColumnPlugin', 'SectionPlugin', 'MediaObjectPlugin']
    allow_children = True

    def render(self, context, instance, placeholder):
        context['size'] = (instance.size.width, instance.size.height)
        context['instance'] = instance
        context['image'] = instance.image
        return context
plugin_pool.register_plugin(MediaObjectPlugin)


class ImagePlugin(CMSPluginBase):
    model = Image
    module = _("Bootstrap4")
    name = _("Image")
    render_template = "bootstrap4/image.html"
    parent_classes = ['ColumnPlugin', 'SectionPlugin', 'MediaObjectPlugin']
    allow_children = True

    def render(self, context, instance, placeholder):
        context['size'] = (instance.size.width, instance.size.height)
        context['instance'] = instance
        context['image'] = instance.image
        context['css'] = instance.get_css()
        return context
plugin_pool.register_plugin(ImagePlugin)


class EmbedPlugin(CMSPluginBase):
    model = Embed
    module = _("Bootstrap4")
    name = _("Embed")
    render_template = "bootstrap4/embed.html"
    parent_classes = ['ColumnPlugin', 'SectionPlugin', 'MediaObjectPlugin']
    allow_children = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
plugin_pool.register_plugin(EmbedPlugin)
