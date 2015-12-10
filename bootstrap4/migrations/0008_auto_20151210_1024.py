# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0007_column'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='min_height',
        ),
        migrations.AlterField(
            model_name='column',
            name='hidden',
            field=models.CharField(default=b'', choices=[(b'', 'Always visible'), (b'hidden-sm-down', 'hidden-sm-down'), (b'hidden-sm-up', 'hidden-sm-up'), (b'hidden-md-down', 'hidden-md-down'), (b'hidden-md-up', 'hidden-md-up'), (b'hidden-lg-down', 'hidden-lg-down'), (b'hidden-lg-up', 'hidden-lg-up')], max_length=20, blank=True, null=True, verbose_name='Hilde Column'),
        ),
    ]
