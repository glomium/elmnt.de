# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailform',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('site_email', models.EmailField(max_length=75, verbose_name='Email recipient')),
                ('formular', models.CharField(default=b'cmsplugin_mailform.examples.ContactForm', max_length=200, verbose_name='Form', choices=[(b'mailform.examples.ContactForm', 'Contactform')])),
                ('success_page', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Success page', to='cms.Page', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
