# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technologies', '0004_removed_taggit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technology',
            name='placeholder',
        ),
    ]
