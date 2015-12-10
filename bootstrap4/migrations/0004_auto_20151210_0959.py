# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0003_auto_20151210_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='container',
            field=models.CharField(default=b'c', choices=[(b'c', 'Fixed'), (b'f', 'Flexible')], max_length=1, blank=True, null=True, verbose_name='Container'),
        ),
    ]
