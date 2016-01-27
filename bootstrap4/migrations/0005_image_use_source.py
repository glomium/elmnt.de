# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0004_button'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='use_source',
            field=models.BooleanField(default=False, verbose_name='Use Source-Image'),
        ),
    ]
