#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool

from .models import Technology


class TechnologyMenu(CMSAttachMenu):
    name = _("Technology Menu")

    def get_nodes(self, request):
        nodes = []
        for technology in Technology.active.all():
            node = NavigationNode(
                technology.name,
                technology.get_absolute_url(),
                technology.pk
            )
            nodes.append(node)
        return nodes
menu_pool.register_menu(TechnologyMenu)
