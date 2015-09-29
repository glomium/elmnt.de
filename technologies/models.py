#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager


class TechnologyManager(models.Manager):

    def get_queryset(self):
        qs = super(TechnologyManager, self).get_queryset()
        qs = qs.filter(published=True)
        qs = qs.prefetch_related('logo')
        return qs


@python_2_unicode_compatible
class Technology(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100,
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=100,
        blank=False,
        unique=True,
    )
    skill = models.PositiveSmallIntegerField(
        _('Skill'),
        blank=False,
    )
    logo = FilerImageField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Logo"),
        on_delete=models.SET_NULL,
    )
    homepage = models.URLField(
        _('Homepage'),
        blank=True,
    )
    text = models.CharField(
        _('Help Text'),
        max_length=255,
        blank=True,
        null=True,
    )
    display_name = models.BooleanField(
        _('Display Name'),
        default=True,
    )

    placeholder = PlaceholderField('technologies_placeholder')

    tags = TaggableManager(blank=True)

    published = models.BooleanField(_("Is published"), default=True)

    modified = models.DateTimeField(
        _("Modified"),
        auto_now=True,
        editable=False,
        null=True,
        blank=False,
    )

    created = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        editable=False,
        null=True,
        blank=False,
    )

    objects = models.Manager()
    active = TechnologyManager()

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = _('Technologies')
        verbose_name = _('Technology')
        ordering = ['name']

    def object_has_logo(self):
        return bool(self.logo_id)
    object_has_logo.boolean = True
    object_has_logo.short_description = _('Logo?')

    @models.permalink
    def get_absolute_url(self):
        return ('technologies-detail', None, {
            'slug': self.slug
        })
