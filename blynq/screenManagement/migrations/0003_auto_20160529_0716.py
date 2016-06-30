# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0002_auto_20160528_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='screenactivationkey',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='screenactivationkey',
            name='device_serial_num',
            field=models.CharField(max_length=20, unique=True, null=True),
        ),
    ]
