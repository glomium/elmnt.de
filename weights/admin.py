#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Profile
from .models import Data

class DataAdmin(admin.ModelAdmin):
    readonly_fields = (
        'calc_vweight',
        'calc_dweight',
        'calc_vslope',
        'calc_dslope',
        'calc_vbmi',
        'calc_dbmi',
        'max_weight',
        'min_weight',
    )
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'weight'),
        }),
        (_('Calclulated'), {
            'classes': ('collapse',),
            'fields': readonly_fields
        }),
    )
    list_display = ('date', 'user', 'weight', 'calc_vweight', 'calc_vbmi', 'max_weight', 'min_weight')
    list_display_links = ('date',)

admin.site.register(Profile)
admin.site.register(Data, DataAdmin)
