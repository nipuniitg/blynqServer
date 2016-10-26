# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0019_remove_schedule_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='layout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='layoutManagement.Layout', null=True),
        ),
        migrations.AlterField(
            model_name='schedulepane',
            name='layout_pane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='layoutManagement.LayoutPane', null=True),
        ),
    ]
