# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weights', '0004_auto_20160114_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='data',
            name='weight',
            field=models.DecimalField(help_text='Enter your todays weight (XXX.X)', verbose_name='Weight', max_digits=4, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.DecimalField(help_text='Your height is used for calculating your BMI (X.XXX m)', verbose_name='Height', max_digits=4, decimal_places=3),
        ),
    ]
