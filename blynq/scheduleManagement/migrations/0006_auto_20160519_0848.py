# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0005_schedule_all_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulescreens',
            name='event',
            field=models.ForeignKey(related_name='schedulescreens', on_delete=django.db.models.deletion.PROTECT, to='schedule.Event', null=True),
        ),
    ]
