#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField
from filer.fields.image import FilerImageField

STATUS_ALPHA = 'a'
STATUS_BETA = 'b'
STATUS_RELEASED = 'r'
STATUS_CHOICES = (
    (STATUS_ALPHA,   _('alpha')),
    (STATUS_BETA, _('beta')),
    (STATUS_RELEASED, _('released')),
)

class ProjectsManager(models.Manager):

    def get_queryset(self):
        qs = super(ProjectsManager, self).get_queryset()
        qs = qs.filter(published=True)
        qs = qs.prefetch_related('logo')
        return qs

@python_2_unicode_compatible
class Project(models.Model):
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
    logo = FilerImageField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Logo"),
        on_delete=models.SET_NULL,
    )
    status = models.CharField(
        _('Status'),
        max_length=100,
        blank=False,
        null=True,
        choices=STATUS_CHOICES,
    )
    repository = models.URLField(
        _('Repository'),
        blank=True,
    )
    homepage = models.URLField(
        _('Homepage'),
        blank=True,
    )
    placeholder = PlaceholderField('projects_placeholder')

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
    on_site = ProjectsManager()

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = _('Projects')
        verbose_name = _('Project')
        ordering = ['name']

    def object_has_logo(self):
        return bool(self.logo_id)
    object_has_logo.boolean = True
    object_has_logo.short_description = _('Logo?')

    @models.permalink
    def get_absolute_url(self):
        return ('projects-detail', None, {
            'slug': self.slug
        })
