# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0020_auto_20161025_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='schedule_description',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
