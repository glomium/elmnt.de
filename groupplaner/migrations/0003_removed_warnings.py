# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupplaner', '0002_auto_20141209_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='changed',
            field=models.DateTimeField(auto_now=True, verbose_name='changed'),
        ),
    ]
