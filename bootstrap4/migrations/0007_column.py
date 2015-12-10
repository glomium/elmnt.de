# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('bootstrap4', '0006_row'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('xs', models.CharField(default=b'col-xs-12', max_length=10, null=True, verbose_name='Phone', choices=[(b'col-xs-1', 'One Gridpoint'), (b'col-xs-2', 'Two Gridpoints'), (b'col-xs-3', '3 Gridpoints'), (b'col-xs-4', '4 Gridpoints'), (b'col-xs-5', '5 Gridpoints'), (b'col-xs-6', '6 Gridpoints'), (b'col-xs-7', '7 Gridpoints'), (b'col-xs-8', '8 Gridpoints'), (b'col-xs-9', '9 Gridpoints'), (b'col-xs-10', '10 Gridpoints'), (b'col-xs-11', '11 Gridpoints'), (b'col-xs-12', '12 Gridpoints')])),
                ('sm', models.CharField(default=b'', choices=[(b'', 'Use breakpoint from smaller grid'), (b'col-sm-1', 'One Gridpoint'), (b'col-sm-2', 'Two Gridpoints'), (b'col-sm-3', '3 Gridpoints'), (b'col-sm-4', '4 Gridpoints'), (b'col-sm-5', '5 Gridpoints'), (b'col-sm-6', '6 Gridpoints'), (b'col-sm-7', '7 Gridpoints'), (b'col-sm-8', '8 Gridpoints'), (b'col-sm-9', '9 Gridpoints'), (b'col-sm-10', '10 Gridpoints'), (b'col-sm-11', '11 Gridpoints'), (b'col-sm-12', '12 Gridpoints')], max_length=10, blank=True, null=True, verbose_name='Tablet')),
                ('md', models.CharField(default=b'', choices=[(b'', 'Use breakpoint from smaller grid'), (b'col-md-1', 'One Gridpoint'), (b'col-md-2', 'Two Gridpoints'), (b'col-md-3', '3 Gridpoints'), (b'col-md-4', '4 Gridpoints'), (b'col-md-5', '5 Gridpoints'), (b'col-md-6', '6 Gridpoints'), (b'col-md-7', '7 Gridpoints'), (b'col-md-8', '8 Gridpoints'), (b'col-md-9', '9 Gridpoints'), (b'col-md-10', '10 Gridpoints'), (b'col-md-11', '11 Gridpoints'), (b'col-md-12', '12 Gridpoints')], max_length=10, blank=True, null=True, verbose_name='Laptop')),
                ('lg', models.CharField(default=b'', choices=[(b'', 'Use breakpoint from smaller grid'), (b'col-lg-1', 'One Gridpoint'), (b'col-lg-2', 'Two Gridpoints'), (b'col-lg-3', '3 Gridpoints'), (b'col-lg-4', '4 Gridpoints'), (b'col-lg-5', '5 Gridpoints'), (b'col-lg-6', '6 Gridpoints'), (b'col-lg-7', '7 Gridpoints'), (b'col-lg-8', '8 Gridpoints'), (b'col-lg-9', '9 Gridpoints'), (b'col-lg-10', '10 Gridpoints'), (b'col-lg-11', '11 Gridpoints'), (b'col-lg-12', '12 Gridpoints')], max_length=10, blank=True, null=True, verbose_name='Desktop')),
                ('xl', models.CharField(default=b'', choices=[(b'', 'Use breakpoint from smaller grid'), (b'col-xl-1', 'One Gridpoint'), (b'col-xl-2', 'Two Gridpoints'), (b'col-xl-3', '3 Gridpoints'), (b'col-xl-4', '4 Gridpoints'), (b'col-xl-5', '5 Gridpoints'), (b'col-xl-6', '6 Gridpoints'), (b'col-xl-7', '7 Gridpoints'), (b'col-xl-8', '8 Gridpoints'), (b'col-xl-9', '9 Gridpoints'), (b'col-xl-10', '10 Gridpoints'), (b'col-xl-11', '11 Gridpoints'), (b'col-xl-12', '12 Gridpoints')], max_length=10, blank=True, null=True, verbose_name='Large Desktop')),
                ('hidden', models.CharField(default=b'', choices=[(b'', 'Always visible'), (b'hidden-xs', 'Hidden on Phones'), (b'hidden-sm hidden-xs', 'Hidden on Tablets and Phones'), (b'visible-lg', 'Visible only on large displays')], max_length=20, blank=True, null=True, verbose_name='Hilde Column')),
                ('min_height', models.PositiveIntegerField(null=True, verbose_name='Minimum Height', blank=True)),
                ('css', models.CharField(default=b'', max_length=40, null=True, verbose_name='Additional class', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
