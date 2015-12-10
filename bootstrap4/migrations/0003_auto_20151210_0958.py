# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0002_auto_20151210_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='in_navigation',
            field=models.BooleanField(default=False, help_text=b'has no effect - yet', verbose_name='In navigation?'),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Name', blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(max_length=200, null=True, verbose_name='Slug', blank=True),
        ),
    ]
