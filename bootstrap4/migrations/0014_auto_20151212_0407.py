# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
        ('bootstrap4', '0013_auto_20151212_0349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('crop', models.BooleanField(default=True, verbose_name='Crop')),
                ('upscale', models.BooleanField(default=True, verbose_name='Upscale')),
                ('responsive', models.BooleanField(default=True, verbose_name='Responsive')),
                ('align', models.CharField(default=b'c', max_length=1, verbose_name='Align', choices=[(b'l', 'Left'), (b'c', 'Center'), (b'r', 'Right')])),
                ('shape', models.CharField(default=b'r', max_length=1, verbose_name='Shape', choices=[(b'r', 'Rounded'), (b'n', 'No style'), (b'c', 'Circle'), (b't', 'Thumbnail')])),
                ('css', models.CharField(default=b'', max_length=40, null=True, verbose_name='Additional class', blank=True)),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', null=True, verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='imagewidth',
            name='plugin',
            field=models.CharField(db_index=True, max_length=16, verbose_name='Plugin', choices=[(b'mediaobject', 'MediaObject'), (b'image', 'Image')]),
        ),
        migrations.AddField(
            model_name='image',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Size', to='bootstrap4.ImageWidth'),
        ),
    ]
