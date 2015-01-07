#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool

from .models import Project


class ProjectMenu(CMSAttachMenu):
    name = _("Project Menu")

    def get_nodes(self, request):
        nodes = []
        for project in Project.active.all():
            print '*'*80
            print '*'*80
            print project
            print '*'*80
            print '*'*80
            node = NavigationNode(
                project.name,
                project.get_absolute_url(),
                project.pk
            )
            nodes.append(node)
        return nodes
menu_pool.register_menu(ProjectMenu)
