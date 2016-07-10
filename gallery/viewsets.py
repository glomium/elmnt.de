#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets
# from rest_framework.decorators import detail_route
# from rest_framework.decorators import list_route
# from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer


class PhotoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_value_regex = '[\w-]+' 
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
