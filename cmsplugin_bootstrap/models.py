# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from cms.models import CMSPlugin


GRID_XS = (
    ('col-xs-1', _('One Gridpoint')),
    ('col-xs-2', _('Two Gridpoints')),
    ('col-xs-3', _('3 Gridpoints')),
    ('col-xs-4', _('4 Gridpoints')),
    ('col-xs-5', _('5 Gridpoints')),
    ('col-xs-6', _('6 Gridpoints')),
    ('col-xs-7', _('7 Gridpoints')),
    ('col-xs-8', _('8 Gridpoints')),
    ('col-xs-9', _('9 Gridpoints')),
    ('col-xs-10', _('10 Gridpoints')),
    ('col-xs-11', _('11 Gridpoints')),
    ('col-xs-12', _('12 Gridpoints')),
)


GRID_SM = (
    ('', _('Use breakpoint from smaller grid')),
    ('col-sm-1', _('One Gridpoint')),
    ('col-sm-2', _('Two Gridpoints')),
    ('col-sm-3', _('3 Gridpoints')),
    ('col-sm-4', _('4 Gridpoints')),
    ('col-sm-5', _('5 Gridpoints')),
    ('col-sm-6', _('6 Gridpoints')),
    ('col-sm-7', _('7 Gridpoints')),
    ('col-sm-8', _('8 Gridpoints')),
    ('col-sm-9', _('9 Gridpoints')),
    ('col-sm-10', _('10 Gridpoints')),
    ('col-sm-11', _('11 Gridpoints')),
    ('col-sm-12', _('12 Gridpoints')),
)


GRID_MD = (
    ('', _('Use breakpoint from smaller grid')),
    ('col-md-1', _('One Gridpoint')),
    ('col-md-2', _('Two Gridpoints')),
    ('col-md-3', _('3 Gridpoints')),
    ('col-md-4', _('4 Gridpoints')),
    ('col-md-5', _('5 Gridpoints')),
    ('col-md-6', _('6 Gridpoints')),
    ('col-md-7', _('7 Gridpoints')),
    ('col-md-8', _('8 Gridpoints')),
    ('col-md-9', _('9 Gridpoints')),
    ('col-md-10', _('10 Gridpoints')),
    ('col-md-11', _('11 Gridpoints')),
    ('col-md-12', _('12 Gridpoints')),
)


GRID_LG = (
    ('', _('Use breakpoint from smaller grid')),
    ('col-lg-1', _('One Gridpoint')),
    ('col-lg-2', _('Two Gridpoints')),
    ('col-lg-3', _('3 Gridpoints')),
    ('col-lg-4', _('4 Gridpoints')),
    ('col-lg-5', _('5 Gridpoints')),
    ('col-lg-6', _('6 Gridpoints')),
    ('col-lg-7', _('7 Gridpoints')),
    ('col-lg-8', _('8 Gridpoints')),
    ('col-lg-9', _('9 Gridpoints')),
    ('col-lg-10', _('10 Gridpoints')),
    ('col-lg-11', _('11 Gridpoints')),
    ('col-lg-12', _('12 Gridpoints')),
)


GRID_HIDDEN = (
    ('', _('Always visible')),
    ('hidden-xs', _('Hidden on Phones')),
    ('hidden-sm hidden-xs', _('Hidden on Tablets and Phones')),
    ('visible-lg', _('Visible only on large displays')),
)


WELL_TYPES = (
    ('', _('Default')),
    ('well-sm', _('Small')),
    ('well-lg', _('Large')),
)


@python_2_unicode_compatible
class Row(CMSPlugin):
    """
    """
    css = models.CharField(
        _('Additional class'),
        default='',
        max_length=40,
        blank=True,
        null=True,
    )

    def __str__(self):
        num_cols = self.get_children().count()
        return ungettext_lazy('with {0} column', 'with {0} columns', num_cols).format(num_cols)


@python_2_unicode_compatible
class Column(CMSPlugin):
    """
    """
    xs = models.CharField(
        _('Phone'),
        choices=GRID_XS,
        default=GRID_XS[-1][0],
        max_length=10,
        blank=False,
        null=True,
    )
    sm = models.CharField(
        _('Tablet'),
        choices=GRID_SM,
        default='',
        max_length=10,
        blank=True,
        null=True,
    )
    md = models.CharField(
        _('Laptop'),
        choices=GRID_MD,
        default='',
        max_length=10,
        blank=True,
        null=True,
    )
    lg = models.CharField(
        _('Desktop'),
        choices=GRID_LG,
        default='',
        max_length=10,
        blank=True,
        null=True,
    )
    hidden = models.CharField(
        _('Hilde Column'),
        choices=GRID_HIDDEN,
        default='',
        max_length=20,
        blank=True,
        null=True,
    )
    min_height = models.PositiveIntegerField(
        _('Minimum Height'),
        blank=True,
        null=True,
    )
    css = models.CharField(
        _('Additional class'),
        default='',
        max_length=40,
        blank=True,
        null=True,
    )

    def get_css(self):
        data = [self.xs]
        if self.sm: data.append(self.sm)
        if self.md: data.append(self.md)
        if self.lg: data.append(self.lg)
        if self.hidden: data.append(self.hidden)
        if self.css: data.append(self.css)
        return ' '.join(data)

    def __str__(self):
        return self.get_css()


@python_2_unicode_compatible
class Well(CMSPlugin):
    """
    """
    type = models.CharField(
        _('Well Type'),
        choices=WELL_TYPES,
        default='',
        max_length=10,
        blank=True,
        null=True,
    )
    min_height = models.PositiveIntegerField(
        _('Minimum Height'),
        blank=True,
        null=True,
    )
    css = models.CharField(
        _('Additional class'),
        default='',
        max_length=40,
        blank=True,
        null=True,
    )

    def get_css(self):
        data = []
        if self.type: data.append(self.type)
        if self.css: data.append(self.css)
        return ' '.join(data)

    def __str__(self):
        return self.get_css()
