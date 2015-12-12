# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4', '0012_auto_20151212_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagewidth',
            name='plugin',
            field=models.CharField(db_index=True, max_length=16, verbose_name='Plugin', choices=[(b'mediaobject', 'MediaObject')]),
        ),
    ]
