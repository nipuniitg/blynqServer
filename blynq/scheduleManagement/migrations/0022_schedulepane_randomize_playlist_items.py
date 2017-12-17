# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0021_schedule_schedule_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulepane',
            name='randomize_playlist_items',
            field=models.BooleanField(default=False),
        ),
    ]
