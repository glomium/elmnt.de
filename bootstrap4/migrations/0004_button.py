# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djangocms_link.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('bootstrap4', '0003_auto_20160125_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('url', models.CharField(blank=True, max_length=2048, null=True, verbose_name='link', validators=[djangocms_link.validators.IntranetURLValidator(intranet_host_re=None)])),
                ('anchor', models.CharField(help_text='This applies only to page and text links. Do <em>not</em> include a preceding "#" symbol.', max_length=128, verbose_name='anchor', blank=True)),
                ('mailto', models.EmailField(help_text='An email address has priority over a text link.', max_length=254, null=True, verbose_name='email address', blank=True)),
                ('phone', models.CharField(help_text='A phone number has priority over a mailto link.', max_length=40, null=True, verbose_name='Phone', blank=True)),
                ('target', models.CharField(blank=True, max_length=100, verbose_name='target', choices=[('', 'same window'), ('_blank', 'new window'), ('_parent', 'parent window'), ('_top', 'topmost frame')])),
                ('size', models.CharField(default=b'', max_length=5, verbose_name='size', blank=True, choices=[(b'', 'Normal'), (b'lg', 'Large'), (b'sm', 'Small')])),
                ('color', models.CharField(default=b'secondary', max_length=20, null=True, verbose_name='color', choices=[(b'primary', 'Primary'), (b'secondary', 'Secondary'), (b'success', 'Success'), (b'info', 'Info'), (b'warning', 'Warning'), (b'danger', 'Danger'), (b'primary-outline', 'Primary Outline'), (b'secondary-outline', 'Secondary Outline'), (b'success-outline', 'Success Outline'), (b'info-outline', 'Info Outline'), (b'warning-outline', 'Warning Outline'), (b'danger-outline', 'Danger Outline')])),
                ('page_link', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='A link to a page has priority over a text link.', null=True, verbose_name='page')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
