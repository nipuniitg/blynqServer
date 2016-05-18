# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0004_auto_20160511_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='all_day',
            field=models.BooleanField(default=True),
        ),
    ]
