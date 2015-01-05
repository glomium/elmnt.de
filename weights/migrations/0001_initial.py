# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Datum')),
                ('weight', models.DecimalField(help_text='Enter your todays weight (XXX.X)', verbose_name='weight', max_digits=4, decimal_places=1)),
                ('calc_vweight', models.FloatField(null=True, verbose_name='calculated weight', blank=True)),
                ('calc_dweight', models.FloatField(null=True, verbose_name='calculated weight error', blank=True)),
                ('calc_vslope', models.FloatField(null=True, verbose_name='calculated slope', blank=True)),
                ('calc_dslope', models.FloatField(null=True, verbose_name='calculated slope error', blank=True)),
                ('calc_vbmi', models.FloatField(null=True, verbose_name='calculated bmi', blank=True)),
                ('calc_dbmi', models.FloatField(null=True, verbose_name='calculated bmi error', blank=True)),
                ('max_weight', models.FloatField(null=True, verbose_name='max weight last two months', blank=True)),
                ('min_weight', models.FloatField(null=True, verbose_name='min weight last two months', blank=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Data',
                'verbose_name_plural': 'Data',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birth', models.DateField(help_text='Your birthday is used to check your target-BMI', verbose_name='birthday')),
                ('gender', models.CharField(help_text='Your gender is used to check yout target-BMI', max_length=1, verbose_name='gender', choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('height', models.DecimalField(help_text='Your height is used for calculating your BMI (X.XXX m)', verbose_name='H\xf6he', max_digits=4, decimal_places=3)),
                ('dheight', models.DecimalField(help_text='The error of your height is used to calculate the error of your BMI (X.XXX m)', verbose_name='delta height', max_digits=4, decimal_places=3)),
                ('bmitarget', models.DecimalField(help_text='Enter Your target BMI (XX.XX)', verbose_name='bmi target', max_digits=4, decimal_places=2)),
                ('user', models.ForeignKey(related_name='+', null=True, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='data',
            name='user',
            field=models.ForeignKey(related_name='data', to='weights.Profile', unique_for_date=b'date'),
            preserve_default=True,
        ),
    ]
