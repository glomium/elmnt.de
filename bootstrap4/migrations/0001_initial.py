# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, null=True, verbose_name='Slug')),
                ('container_fixed', models.BooleanField(default=True, verbose_name='Fixed container?')),
                ('css', models.CharField(max_length=200, null=True, verbose_name='CSS', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
