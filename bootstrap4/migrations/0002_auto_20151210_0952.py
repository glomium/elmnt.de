# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='container_fixed',
        ),
        migrations.AddField(
            model_name='section',
            name='container',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Container', choices=[(b'c', 'Fixed'), (b'f', 'Flexible')]),
        ),
    ]
