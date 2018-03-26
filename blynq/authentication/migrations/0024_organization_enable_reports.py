# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0023_auto_20170301_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='enable_reports',
            field=models.BooleanField(default=False),
        ),
    ]
