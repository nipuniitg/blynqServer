# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0012_schedule_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulepane',
            name='event',
            field=models.OneToOneField(related_name='schedulepane_event', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='schedule.Event'),
        ),
    ]
