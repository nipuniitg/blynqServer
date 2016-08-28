# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playerManagement', '0006_auto_20160821_0858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerupdate',
            name='last_modified_time',
        ),
        migrations.AddField(
            model_name='playerupdate',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at', null=True),
        ),
    ]
