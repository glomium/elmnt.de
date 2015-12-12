# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-status', 'name'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=1, null=True, verbose_name='Status', choices=[(b'a', 'alpha'), (b'b', 'beta'), (b'r', 'released')]),
        ),
    ]
