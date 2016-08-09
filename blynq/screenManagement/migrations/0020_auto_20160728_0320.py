# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0019_screen_last_active_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='last_active_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
