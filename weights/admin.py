#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib import admin

from .models import Profile, Data, Month

class DataAdmin(admin.ModelAdmin):
  fields = ('user', 'date', 'weight')

admin.site.register(Profile)
admin.site.register(Data, DataAdmin)
admin.site.register(Month)
