# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0002_embed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embed',
            name='source',
            field=models.CharField(max_length=255, null=True, verbose_name='Source'),
        ),
    ]
