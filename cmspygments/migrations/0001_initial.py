# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cmspygments.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='PygmentsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('code_language', cmspygments.models.ChoicesCharField(default=b'text', max_length=20)),
                ('code', models.TextField()),
                ('linenumbers', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
