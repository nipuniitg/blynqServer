# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0011_auto_20160726_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
