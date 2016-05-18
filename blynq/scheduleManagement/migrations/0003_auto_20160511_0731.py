# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0002_auto_20160510_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='is_always',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='recurrence_absolute',
            field=models.BooleanField(default=False),
        ),
    ]
