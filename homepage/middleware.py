# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.cache import patch_vary_headers


class DoNotTrackMiddleware(object):
    """
    Sets request.dnt to True or False based on the presence of the
    DNT HTTP header.
    """

    def process_request(self, request):
        if request.META.get('HTTP_DNT', '1') == '1':
            request.DNT = True
        else:
            request.DNT = False

    def process_response(self, request, response):
        # content may depend on DNT
        patch_vary_headers(response, ('DNT',))
        return response
