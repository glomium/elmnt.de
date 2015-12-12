# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
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
                ('hidden', models.CharField(default=b'', choices=[(b'', 'Always visible'), (b'hidden-sm-down', 'hidden-sm-down'), (b'hidden-sm-up', 'hidden-sm-up'), (b'hidden-md-down', 'hidden-md-down'), (b'hidden-md-up', 'hidden-md-up'), (b'hidden-lg-down', 'hidden-lg-down'), (b'hidden-lg-up', 'hidden-lg-up')], max_length=20, blank=True, null=True, verbose_name='Hide Column')),
                ('css', models.CharField(default=b'', max_length=40, null=True, verbose_name='Additional class', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
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
        migrations.CreateModel(
            name='Image',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('crop', models.BooleanField(default=True, verbose_name='Crop')),
                ('upscale', models.BooleanField(default=True, verbose_name='Upscale')),
                ('align', models.CharField(default=b'f', max_length=1, verbose_name='Align', choices=[(b'f', 'Responsive'), (b'l', 'Left'), (b'c', 'Center'), (b'r', 'Right')])),
                ('shape', models.CharField(default=b'r', max_length=1, verbose_name='Shape', choices=[(b'r', 'Rounded'), (b'n', 'No style'), (b'c', 'Circle'), (b't', 'Thumbnail')])),
                ('css', models.CharField(default=b'', max_length=40, null=True, verbose_name='Additional class', blank=True)),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', null=True, verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ImageWidth',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('plugin', models.CharField(db_index=True, max_length=16, verbose_name='Plugin', choices=[(b'mediaobject', 'MediaObject'), (b'image', 'Image')])),
                ('width', models.PositiveIntegerField(verbose_name='Width')),
                ('height', models.PositiveIntegerField(verbose_name='Height')),
            ],
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='MediaObject',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Title')),
                ('crop', models.BooleanField(default=True, verbose_name='Crop')),
                ('upscale', models.BooleanField(default=True, verbose_name='Upscale')),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', null=True, verbose_name='Image')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Size', to='bootstrap4.ImageWidth')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('css', models.CharField(default=b'', max_length=40, null=True, verbose_name='Additional class', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name', blank=True)),
                ('slug', models.SlugField(max_length=200, null=True, verbose_name='Slug', blank=True)),
                ('in_navigation', models.BooleanField(default=False, help_text=b'has no effect - yet', verbose_name='In navigation?')),
                ('container', models.CharField(default=b'c', choices=[(b'c', 'Fixed'), (b'f', 'Fluid')], max_length=1, blank=True, null=True, verbose_name='Container')),
                ('css', models.CharField(max_length=200, null=True, verbose_name='CSS', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterUniqueTogether(
            name='imagewidth',
            unique_together=set([('plugin', 'width', 'height')]),
        ),
        migrations.AddField(
            model_name='image',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Size', to='bootstrap4.ImageWidth'),
        ),
    ]
