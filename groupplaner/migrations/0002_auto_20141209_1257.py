# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groupplaner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='weekly',
            field=models.ForeignKey(related_name='+', blank=True, to='groupplaner.WeeklyEvent', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='participent',
            name='user',
            field=models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
