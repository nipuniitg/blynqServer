# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0014_auto_20160728_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='layout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='layoutManagement.Layout', null=True),
        ),
    ]
