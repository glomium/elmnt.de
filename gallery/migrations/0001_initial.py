# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='date', blank=True)),
                ('slug', models.SlugField(unique=True, verbose_name='slug', blank=True)),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, verbose_name='Image', to='filer.Image', null=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
        ),
    ]
