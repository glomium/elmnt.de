# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
        ('bootstrap4', '0009_auto_20151210_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaObject',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Title')),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', null=True, verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
