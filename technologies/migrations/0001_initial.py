# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('status', models.CharField(max_length=100, null=True, verbose_name='Status', choices=[(b'a', 'alpha'), (b'b', 'beta'), (b'r', 'released')])),
                ('repository', models.URLField(verbose_name='Repository', blank=True)),
                ('homepage', models.URLField(verbose_name='Homepage', blank=True)),
                ('published', models.BooleanField(default=True, verbose_name='Is published')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('logo', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='filer.Image', null=True, verbose_name='Logo')),
                ('placeholder', cms.models.fields.PlaceholderField(slotname=b'projects_placeholder', editable=False, to='cms.Placeholder', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
    ]
