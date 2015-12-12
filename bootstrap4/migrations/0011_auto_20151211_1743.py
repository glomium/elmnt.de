# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0010_mediaobject'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaobject',
            name='crop',
            field=models.BooleanField(default=True, verbose_name='Crop'),
        ),
        migrations.AddField(
            model_name='mediaobject',
            name='upscale',
            field=models.BooleanField(default=True, verbose_name='Upscale'),
        ),
    ]
