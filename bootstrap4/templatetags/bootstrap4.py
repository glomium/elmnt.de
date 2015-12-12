#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Library
from django.template import Node


register = Library()


@register.assignment_tag(takes_context=True)
def get_bootstrap_anchors(context, placeholder="content", plugin="SectionPlugin"):
    if 'current_page' not in context:
        return []
    return context['current_page'].placeholders.get(slot=placeholder).get_plugins().filter(plugin_type=plugin).order_by('position').values_list('section__slug', 'section__name')


# TODO:
# LOAD A LIST FROM A PAGE WHICH CONTAINS ALL
# Sections WITH THEIR name AND slug ATTRIBUTES
# USED TO GENERATE A NAVIGATIONBAR
# WITH INTERNAL CONTENT

