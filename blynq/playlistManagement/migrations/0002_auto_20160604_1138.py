# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='playlist_total_time',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
