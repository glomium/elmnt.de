# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technologies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='text',
            field=models.CharField(max_length=255, null=True, verbose_name='Help Text', blank=True),
        ),
    ]
