# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('bootstrap4', '0011_auto_20151211_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageWidth',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('plugin', models.CharField(max_length=16, verbose_name='Plugin', choices=[(b'mediaobject', 'MediaObject')])),
                ('width', models.PositiveIntegerField(verbose_name='Width')),
                ('height', models.PositiveIntegerField(verbose_name='Height')),
            ],
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterUniqueTogether(
            name='imagewidth',
            unique_together=set([('plugin', 'width', 'height')]),
        ),
        migrations.AddField(
            model_name='mediaobject',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=0, verbose_name='Size', to='bootstrap4.ImageWidth'),
            preserve_default=False,
        ),
    ]
