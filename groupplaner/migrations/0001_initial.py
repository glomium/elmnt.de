# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=1, verbose_name='day', choices=[(b'0', 'Monday'), (b'1', 'Tuesday'), (b'2', 'Wednesday'), (b'3', 'Thursday'), (b'4', 'Friday'), (b'5', 'Saturday'), (b'6', 'Sunday')])),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('location', models.CharField(max_length=100, verbose_name='location', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('start', models.TimeField(verbose_name='start')),
                ('end', models.TimeField(verbose_name='end')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'ordering': [b'active', b'day', b'start', b'end'],
                'verbose_name': 'Weekly event',
                'verbose_name_plural': 'Weekly events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekly', models.ForeignKey(to_field='id', blank=True, to='groupplaner.WeeklyEvent', null=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('location', models.CharField(max_length=100, verbose_name='location', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('end', models.DateTimeField(verbose_name='end')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='changed', auto_now_add=True)),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
            ],
            options={
                'ordering': [b'start', b'end'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='groupplaner.Event', to_field='id')),
                ('user', models.ForeignKey(to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(1, 'yes'), (3, 'maybe'), (5, 'no')])),
                ('comment', models.CharField(max_length=255, verbose_name='comment', blank=True)),
            ],
            options={
                'ordering': [b'event', b'status'],
                'verbose_name': 'Participent',
                'verbose_name_plural': 'Participents',
            },
            bases=(models.Model,),
        ),
    ]
