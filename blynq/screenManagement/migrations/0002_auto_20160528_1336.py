# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='screenManagement.ScreenStatus', null=True),
        ),
    ]
