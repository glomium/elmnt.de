# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('bootstrap4', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embed',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('source', models.BooleanField(default=True, verbose_name='Source')),
                ('allow_fullscreen', models.BooleanField(default=False, verbose_name='Allow fullscreen')),
                ('ratio', models.CharField(default=b'16by9', max_length=5, verbose_name='Ratio', choices=[(b'21by9', '21:9'), (b'16by9', '16:9'), (b'4by3', '4:3'), (b'1by1', '1:1')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
