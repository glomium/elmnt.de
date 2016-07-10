#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework import serializers

from .models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ('url', 'date', 'slug', 'image')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }

    def get_image(self, obj):
        if obj and obj.image:
           return obj.image.url
        return ''
