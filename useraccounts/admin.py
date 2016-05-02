#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Email
from .models import User


admin.site.register(User, UserAdmin)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_primary', 'is_valid', 'validated', 'updated', 'created')
    list_filter = ('is_primary', 'is_valid')
