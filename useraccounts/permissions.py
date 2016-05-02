#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework import permissions


class EmailPermissions(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # update email address to primary
        if request.method in ['PUT', 'PATCH']:
            return not obj.is_primary and obj.is_valid

        # delete email address
        if request.method in ['DELETE']:
            return not obj.is_primary

        return True
