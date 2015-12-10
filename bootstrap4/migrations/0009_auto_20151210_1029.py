# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('bootstrap4', '0008_auto_20151210_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnClearfix',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('hidden', models.CharField(default=b'', choices=[(b'', 'Always visible'), (b'hidden-sm-down', 'hidden-sm-down'), (b'hidden-sm-up', 'hidden-sm-up'), (b'hidden-md-down', 'hidden-md-down'), (b'hidden-md-up', 'hidden-md-up'), (b'hidden-lg-down', 'hidden-lg-down'), (b'hidden-lg-up', 'hidden-lg-up')], max_length=20, blank=True, null=True, verbose_name='Hidden')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='column',
            name='hidden',
            field=models.CharField(default=b'', choices=[(b'', 'Always visible'), (b'hidden-sm-down', 'hidden-sm-down'), (b'hidden-sm-up', 'hidden-sm-up'), (b'hidden-md-down', 'hidden-md-down'), (b'hidden-md-up', 'hidden-md-up'), (b'hidden-lg-down', 'hidden-lg-down'), (b'hidden-lg-up', 'hidden-lg-up')], max_length=20, blank=True, null=True, verbose_name='Hide Column'),
        ),
    ]
