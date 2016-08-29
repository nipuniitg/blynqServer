# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_mediaanalytics_total_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediaanalytics',
            old_name='total_time',
            new_name='time_played',
        ),
    ]
