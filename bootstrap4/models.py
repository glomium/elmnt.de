# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from filer.fields.image import FilerImageField

from cms.models import CMSPlugin
from djangocms_link.models import AbstractLink


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


GRID_XL = (
    ('', _('Use breakpoint from smaller grid')),
    ('col-xl-1', _('One Gridpoint')),
    ('col-xl-2', _('Two Gridpoints')),
    ('col-xl-3', _('3 Gridpoints')),
    ('col-xl-4', _('4 Gridpoints')),
    ('col-xl-5', _('5 Gridpoints')),
    ('col-xl-6', _('6 Gridpoints')),
    ('col-xl-7', _('7 Gridpoints')),
    ('col-xl-8', _('8 Gridpoints')),
    ('col-xl-9', _('9 Gridpoints')),
    ('col-xl-10', _('10 Gridpoints')),
    ('col-xl-11', _('11 Gridpoints')),
    ('col-xl-12', _('12 Gridpoints')),
)


GRID_HIDDEN = (
    ('', _('Always visible')),
    ('hidden-sm-down', _('hidden-sm-down')),
    ('hidden-sm-up', _('hidden-sm-up')),
    ('hidden-md-down', _('hidden-md-down')),
    ('hidden-md-up', _('hidden-md-up')),
    ('hidden-lg-down', _('hidden-lg-down')),
    ('hidden-lg-up', _('hidden-lg-up')),
)


@python_2_unicode_compatible
class ImageWidth(CMSPlugin):
    """
    """
    PLUGINS = (
        ('mediaobject', _("MediaObject")),
        ('image', _("Image")),
    )
    plugin = models.CharField(
        _('Plugin'),
        max_length=16,
        blank=False,
        null=False,
        choices=PLUGINS,
        db_index=True,
    )
    width = models.PositiveIntegerField(
        _('Width'),
        blank=False,
        null=False,
    )
    height = models.PositiveIntegerField(
        _('Height'),
        blank=False,
        null=False,
    )

    class Meta:
        unique_together = (('plugin', 'width', 'height'),)

    def __str__(self):
        return '%sx%s Pixel' % (self.width, self.height)


@python_2_unicode_compatible
class Section(CMSPlugin):
    """
    """
    CONTAINER_FLUID = 'f'
    CONTAINER_FIXED = 'c'

    name = models.CharField(
        _('Name'),
        max_length=200,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        _('Slug'),
        max_length=200,
        blank=True,
        null=True,
    )

    in_navigation = models.BooleanField(
        _('In navigation?'),
        default=False,
        help_text="has no effect - yet",  # TODO
    )

    container = models.CharField(
        _('Container'),
        max_length=1,
        blank=True,
        null=True,
        choices=(
            (CONTAINER_FIXED, _('Fixed')),
            (CONTAINER_FLUID, _('Fluid')),
        ),
        default=CONTAINER_FIXED,
    )

    css = models.CharField(
        _('CSS'),
        max_length=200,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.slug or 'Plugin'

    def get_container(self):
        if self.container == self.CONTAINER_FIXED:
            return 'container'
        elif self.container == self.CONTAINER_FLUID:
            return 'container-fluid'
        return None

    def get_css(self):
        data = []
        # if self.background: data.append(self.background)
        if self.css: data.append(self.css)
        return ' '.join(data)


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
    xl = models.CharField(
        _('Large Desktop'),
        choices=GRID_XL,
        default='',
        max_length=10,
        blank=True,
        null=True,
    )
    hidden = models.CharField(
        _('Hide Column'),
        choices=GRID_HIDDEN,
        default='',
        max_length=20,
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
        if self.xl: data.append(self.xl)
        if self.hidden: data.append(self.hidden)
        if self.css: data.append(self.css)
        return ' '.join(data)

    def __str__(self):
        return self.get_css()


@python_2_unicode_compatible
class ColumnClearfix(CMSPlugin):
    """
    """
    hidden = models.CharField(
        _('Hidden'),
        choices=GRID_HIDDEN,
        default='',
        max_length=20,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.hidden


class MediaObjectManager(models.Manager):

    def get_queryset(self):
        qs = super(MediaObjectManager, self).get_queryset()
        qs = qs.prefetch_related('image', 'size')
        return qs


@python_2_unicode_compatible
class MediaObject(CMSPlugin):
    """
    """
    title = models.CharField(
        _('Title'),
        max_length=200,
        blank=False,
        null=True,
    )
    picture = FilerImageField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Image"),
        on_delete=models.SET_NULL,
        related_name="+",
    )
    size = models.ForeignKey(
        ImageWidth,
        null=False,
        blank=False,
        verbose_name=_("Size"),
        on_delete=models.PROTECT,
        limit_choices_to={'plugin': 'mediaobject'},
    )

    crop = models.BooleanField(
        _('Crop'),
        default=True,
    )
    upscale = models.BooleanField(
        _('Upscale'),
        default=True,
    )

    objects = MediaObjectManager()

    def __str__(self):
        return self.title or 'Plugin'


class ImageManager(models.Manager):

    def get_queryset(self):
        qs = super(ImageManager, self).get_queryset()
        qs = qs.prefetch_related('image', 'size')
        return qs


@python_2_unicode_compatible
class Image(CMSPlugin):
    """
    """
    picture = FilerImageField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Image"),
        on_delete=models.SET_NULL,
        related_name="+",
    )
    size = models.ForeignKey(
        ImageWidth,
        null=False,
        blank=False,
        verbose_name=_("Size"),
        on_delete=models.PROTECT,
        limit_choices_to={'plugin': 'image'},
    )

    crop = models.BooleanField(
        _('Crop'),
        default=True,
    )
    upscale = models.BooleanField(
        _('Upscale'),
        default=True,
    )

    align = models.CharField(
        _('Align'),
        max_length=1,
        blank=False,
        null=False,
        choices=(
            ('f', _('Responsive')),
            ('l', _('Left')),
            ('c', _('Center')),
            ('r', _('Right')),
        ),
        default='f',
    )

    shape = models.CharField(
        _('Shape'),
        max_length=1,
        blank=False,
        null=False,
        choices=(
            ('r', _('Rounded')),
            ('n', _('No style')),
            ('c', _('Circle')),
            ('t', _('Thumbnail')),
        ),
        default='r',
    )

    css = models.CharField(
        _('Additional class'),
        default='',
        max_length=40,
        blank=True,
        null=True,
    )

    use_source = models.BooleanField(
        _('Use Source-Image'),
        default=False,
    )

    objects = ImageManager()

    def get_css(self):
        image = []
        layer = []

        if self.shape == 'r': image.append('img-rounded')
        elif self.shape == 't': image.append('img-thumbnail')
        elif self.shape == 'c': image.append('img-circle')

        if self.align == 'f':
            image.append('img-fluid')
            image.append('center-block')
        elif self.align == 'c': layer.append('text-xs-left')
        elif self.align == 'l': layer.append('text-xs-left')
        elif self.align == 'r': layer.append('text-xs-right')

        if self.css: image.append(self.css)

        return {
            'image': ' '.join(image),
            'layer': ' '.join(layer),
        }

    def __str__(self):
        return 'Image'


@python_2_unicode_compatible
class Embed(CMSPlugin):
    """
    """
    source = models.CharField(
        _('Source'),
        max_length=255,
        blank=False,
        null=True,
    )
    allow_fullscreen = models.BooleanField(
        _('Allow fullscreen'),
        default=False,
    )

    ratio = models.CharField(
        _('Ratio'),
        max_length=5,
        blank=False,
        null=False,
        choices=(
            ('21by9', _('21:9')),
            ('16by9', _('16:9')),
            ('4by3', _('4:3')),
            ('1by1', _('1:1')),
        ),
        default='16by9',
    )

    def __str__(self):
        if self.source:
            return '%s' % self.source
        else:
            return 'None'


class Button(AbstractLink):
    """
    """
    size = models.CharField(
        _('size'),
        max_length=5,
        blank=True,
        null=False,
        choices=(
            ('', _('Normal')),
            ('lg', _('Large')),
            ('sm', _('Small')),
        ),
        default='',
    )

    color = models.CharField(
        _('color'),
        max_length=20,
        blank=False,
        null=True,
        choices=(
            ('primary', _('Primary')),
            ('secondary', _('Secondary')),
            ('success', _('Success')),
            ('info', _('Info')),
            ('warning', _('Warning')),
            ('danger', _('Danger')),
            ('primary-outline', _('Primary Outline')),
            ('secondary-outline', _('Secondary Outline')),
            ('success-outline', _('Success Outline')),
            ('info-outline', _('Info Outline')),
            ('warning-outline', _('Warning Outline')),
            ('danger-outline', _('Danger Outline')),
        ),
        default='secondary',
    )

    class Meta:
        abstract = False
