# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0015_auto_20160802_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulepane',
            name='mute_audio',
            field=models.BooleanField(default=False),
        ),
    ]
