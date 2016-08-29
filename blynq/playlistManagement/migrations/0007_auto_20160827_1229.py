# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0006_auto_20160825_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created time', null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
