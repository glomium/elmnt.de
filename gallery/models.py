from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver

from datetime import datetime


class Photo(models.Model):
    """ Photo model """
    date = models.DateTimeField(_('date'), blank=True)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, blank=False, related_name="+")
    image = models.ImageField(upload_to='gallery/')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
        ordering  = ['-date']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('gallery-picture', None, {
#           'pk':   self.pk,
            'slug': self.slug,
        })

    def save(self):
        if self.date == None:
            self.date = datetime.now()
        if self.title == '':
            self.title = self.image.name.split('/')[-1]
        if self.slug == '':
            self.slug = '.'.join( self.image.name.split('/')[-1].split('.')[0:-1] )
        super(Photo, self).save()
