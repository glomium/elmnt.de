# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technologies', '0002_technology_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='display_name',
            field=models.BooleanField(default=True, verbose_name='Display Name'),
        ),
    ]
