# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.timezone import make_aware

from filer.fields.image import FilerImageField

from datetime import datetime


class PhotoManager(models.Manager):

    def get_queryset(self):
        qs = super(PhotoManager, self).get_queryset()
        qs = qs.prefetch_related('image')
        return qs


@python_2_unicode_compatible
class Photo(models.Model):
    """ Photo model """
    date = models.DateTimeField(_('date'), blank=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    image = FilerImageField(
        null=True,
        blank=False,
        default=None,
        verbose_name=_("Image"),
        on_delete=models.SET_NULL,
    )
    objects = PhotoManager()

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
        ordering  = ['-date']

    def __str__(self):
        return '%s' % self.image

    @models.permalink
    def get_absolute_url(self):
        return ('gallery-picture', None, {
            'slug': self.slug,
        })

    def clean(self):
        data = self.image._get_exif()

        if not self.slug:
            name = '.'.join( self.image.file.name.split('/')[-1].split('.')[0:-1] )
            self.slug = slugify(name)

        if not self.date:
            date = None
            if 'DateTime' in data:
                date = data['DateTime']
            elif 'DateTimeOriginal' in data:
                date = data['DateTimeOriginal']
            elif 'DateTimeDigitized' in data:
                date = data['DateTimeDigitized']

            if date:
                self.date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
                if settings.USE_TZ:
                    self.date = make_aware(self.date)
            else:
                self.date = now()
