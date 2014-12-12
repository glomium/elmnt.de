#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.contrib import admin

from models import UserProfile, Data, Graph, Month

class DataAdmin(admin.ModelAdmin):
  fields = ('user', 'date', 'weight')

admin.site.register(UserProfile)
admin.site.register(Data, DataAdmin)
admin.site.register(Month)
admin.site.register(Graph)
