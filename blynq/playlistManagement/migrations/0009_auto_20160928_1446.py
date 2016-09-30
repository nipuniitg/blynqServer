# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistitems',
            name='display_time',
            field=models.IntegerField(default=15),
        ),
    ]
