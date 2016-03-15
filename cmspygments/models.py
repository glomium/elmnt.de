from django.db import models
from cms.models import CMSPlugin
from pygments.lexers import get_all_lexers 

from django.utils.functional import lazy


# from pygments.styles import get_all_styles
# STYLE_CHOICES = map(lambda x: (x,x), get_all_styles())


def get_language_choices():
    choices = map(lambda x: (x[1][0], x[0]), get_all_lexers())
    choices.sort(lambda x,y: cmp(x[0], y[0]))
    return choices


class ChoicesCharField(models.CharField):
    def deconstruct(self):
        name, path, args, kwargs = super(ChoicesCharField, self).deconstruct()
        if 'choices' in kwargs:
            del kwargs['choices']
        return name, path, args, kwargs


class PygmentsPlugin(CMSPlugin):
    code_language = ChoicesCharField(
        max_length=20,
        default="text",
        choices=get_language_choices(),
    )
    code = models.TextField()
    linenumbers = models.BooleanField(default=False)
