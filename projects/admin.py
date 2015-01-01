#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib import admin
from models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'repository', 'object_has_logo')
    list_display_links = ('name',)
    list_filter = ('published',)
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Project, ProjectAdmin)
