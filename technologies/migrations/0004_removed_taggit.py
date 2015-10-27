# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from technologies.models import TAGS


def load_tags(apps, schema_editor):
    cls = apps.get_model("technologies", "Tag")
    for key, name in TAGS:
        data, created = cls.objects.get_or_create(tag=key)


class Migration(migrations.Migration):

    dependencies = [
        ('technologies', '0003_technology_display_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=32, verbose_name='Tag', choices=[(b'application', 'Application'), (b'backend', 'Backend'), (b'deployment', 'Deployment'), (b'development', 'Development'), (b'filesystem', 'Filesystem'), (b'frontend', 'Frontend'), (b'javascript', 'Javascript'), (b'python', 'Python'), (b'reporting', 'Reporting'), (b'web', 'Web')])),
            ],
        ),
        migrations.RemoveField(
            model_name='technology',
            name='tags',
        ),
        migrations.AddField(
            model_name='technology',
            name='tags',
            field=models.ManyToManyField(to='technologies.Tag'),
        ),
        migrations.RunPython(load_tags),
    ]
