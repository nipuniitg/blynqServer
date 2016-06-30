# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0006_delete_screenspecs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenactivationkey',
            name='device_serial_num',
            field=models.CharField(max_length=20, unique=True, null=True, blank=True),
        ),
    ]
